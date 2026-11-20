import os
import json
import argparse
import subprocess
import math

def main():
    parser = argparse.ArgumentParser(description="Twitch Chat ve Video Kırpma Aracı")
    parser.add_argument("chat", help="TwitchDownloaderCLI ile indirilen chat.json dosyası")
    parser.add_argument("video", help="Yayın videosu (yayin.mp4)")
    parser.add_argument("--adet", type=int, default=10, help="Maksimum klip sayısı")
    parser.add_argument("--dilim", type=int, default=10, help="Dilim süresi (saniye)")
    parser.add_argument("--once", type=int, default=20, help="Olaydan kaç saniye önce başlasın")
    parser.add_argument("--sure", type=int, default=40, help="Klip süresi (saniye)")
    args = parser.parse_args()

    os.makedirs("klipler", exist_ok=True)

    print("chat.json okunuyor...")
    with open(args.chat, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    comments = data.get("comments", [])
    if not comments:
        print("Hata: chat.json içinde 'comments' listesi bulunamadı veya boş!")
        return

    # Mesajları dilimlere ayır
    bins = {}
    for c in comments:
        offset = c.get("content_offset_seconds", 0)
        bin_idx = int(offset // args.dilim)
        bins[bin_idx] = bins.get(bin_idx, 0) + 1

    if not bins:
        print("Hata: Geçerli mesaj zaman damgası bulunamadı!")
        return

    counts = list(bins.values())
    mean = sum(counts) / len(counts)
    variance = sum((x - mean) ** 2 for x in counts) / len(counts)
    std_dev = math.sqrt(variance) if variance > 0 else 0.0

    threshold = mean + (2 * std_dev)
    print(f"İstatistik -> Ortalama: {mean:.2f}, StdSapma: {std_dev:.2f}, Eşik (Mean + 2*Std): {threshold:.2f}")

    # Eşiği geçen dilimleri filtrele ve yoğunluğa göre sırala
    qualified = []
    for bin_idx, count in bins.items():
        if count >= threshold:
            qualified.append((bin_idx, count))

    qualified.sort(key=lambda x: x[1], reverse=True)

    # 60 saniyeden yakın olanları ele, en fazla `--adet` kadar seç
    selected = []
    for bin_idx, count in qualified:
        moment_sec = bin_idx * args.dilim
        too_close = False
        for _, _, s_moment in selected:
            if abs(moment_sec - s_moment) < 60:
                too_close = True
                break
        if not too_close:
            selected.append((bin_idx, count, moment_sec))
        if len(selected) >= args.adet:
            break

    # Zaman sırasına göre sırala (klip isimleri için)
    selected.sort(key=lambda x: x[2])
    print(f"Seçilen klip sayısı: {len(selected)}")

    for i, (bin_idx, count, moment_sec) in enumerate(selected, 1):
        start_time = max(0, moment_sec - args.once)
        
        m = int(start_time // 60)
        s = int(start_time % 60)
        time_str = f"{m}m{s}s"
        
        out_name = f"klipler/klip_{i:02d}_{time_str}.mp4"
        
        print(f"-> Klip {i}: An={moment_sec}s | Mesaj={count} | Başlangıç={start_time}s | Dosya={out_name}")

        import platform
        ffmpeg_bin = "./ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
        # FFmpeg ile ortadan 9:16 kırp, 1080x1920 ölçekle, sesleri koru
        cmd = [
            ffmpeg_bin, "-y",
            "-ss", str(start_time),
            "-i", args.video,
            "-t", str(args.sure),
            "-vf", "crop=ih*9/16:ih:(in_w-ih*9/16)/2:0,scale=1080:1920",
            "-c:v", "libx264", "-c:a", "aac",
            out_name
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print("İşlem tamamlandı! Klipler 'klipler/' klasörüne kaydedildi.")

if __name__ == "__main__":
    main()