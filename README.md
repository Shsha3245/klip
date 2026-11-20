proje kurulum adımları ilk başta 
https://github.com/lay295/TwitchDownloader/releases buradan klip indirme kısmını indir klasöre ayıkla
.\TwitchDownloaderCLI.exe videodownload --id https://www.twitch.tv/videos/2927702632 -o yayin.mp4 video yayın için terminal
chat için:
 .\TwitchDownloaderCLI.exe chatdownload --id https://www.twitch.tv/videos/2927702632 -o chat.json

 daha sonrasında 
python sohbet_klip.py chat.json yayin.mp4 bunu vsc terminalinde kullan

kick için:
https://github.com/VXsz/ReKick/releases/tag/v1.1.4
.\rekick.exe --url="https://kick.com/asmongold/videos/01a1ead4-4bc0-7343-a892-a2dc424d1707"

daha sonrasında yt-dlp:
https://github.com/yt-dlp/yt-dlp/releases buradan yt-dlp.exe dosyası ana klasöre
kick adresi ile video inmesse eğerki dev tools tan network ve m3u8 ve oradanki linkten dümdüz indirme .\yt-dlp.exe "https://d26yk4zpyhjeeq.cloudfront.net/v1/manifest/a837d8e4b9178bea1b3911d9b2fe01ff7553ef20/production-kick-vod-csb/3bdb0b52-ee6b-498e-9986-c5f1749bc7c3/1.m3u8" -o yayin.mp4
