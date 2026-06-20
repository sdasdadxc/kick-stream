import subprocess
import yt_dlp
import time

YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=Oqr0muaqH0c"
KICK_SERVER = "rtmps://fa723fc1b171.global-contribute.live-video.net/app/sk_us-west-2_MF3RDcWvwV0L_KSgTiQA4tCrDk7CdVqDPNy7ntSWIRX"

while True:
    try:
        print("⚡ Extracting links using Advanced Bypass...")
        
        ydl_opts = {
            # تعديل صيغة السحب لتكون أبسط وأسرع في فك التشفير
            'format': 'best[height<=720]/best',
            'quiet': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_VIDEO_URL, download=False)
            
            # لو الفيديو مدمج فيه الصوت والصورة سوا (وده الأغلب في صيغ البست)
            if 'url' in info and not info.get('requested_formats'):
                video_url = info['url']
                audio_url = info['url']
            else:
                video_url = info['requested_formats'][0]['url']
                audio_url = info['requested_formats'][1]['url']

        print("🚀 Stream is LIVE now on Kick (Skipping first 2 hours)...")
        
        ffmpeg_cmd = [
            'ffmpeg', '-re', 
            '-ss', '7200', '-i', video_url, 
            '-ss', '7200', '-i', audio_url,
            '-map', '0:v:0', '-map', '1:a:0?', # علامة الاستفهام تمنع الفشل لو الصوت والصورة مدمجين في رابط واحد
            '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'ultrafast',
            '-pix_fmt', 'yuv420p', '-g', '60', '-keyint_min', '60', '-sc_threshold', '0',
            '-b:v', '3000k', '-maxrate', '3000k', '-bufsize', '6000k',
            '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2',
            '-f', 'flv', KICK_SERVER
        ]
        subprocess.run(ffmpeg_cmd)
        print("⚠️ Stream disconnected. Reconnecting in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
