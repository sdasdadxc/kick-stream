import subprocess
import yt_dlp
import time

YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=Oqr0muaqH0c"
KICK_SERVER = "rtmps://fa723fc1b171.global-contribute.live-video.net/app/sk_us-west-2_MF3RDcWvwV0L_KSgTiQA4tCrDk7CdVqDPNy7ntSWIRX"

while True:
    try:
        print("⚡ Extracting links using bypass techniques...")
        
        # إعدادات ذكية لتخطي حظر الروبوتات والـ Bot Detection من يوتيوب
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'quiet': True,
            'noplaylist': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'], # محاكاة تشغيل من تطبيق آيفون لتخطي حظر السيرفرات
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_VIDEO_URL, download=False)
            video_url = info['requested_formats'][0]['url']
            audio_url = info['requested_formats'][1]['url']

        print("🚀 Stream is LIVE now on Kick (Skipping first 2 hours)...")
        
        ffmpeg_cmd = [
            'ffmpeg', '-re', 
            '-ss', '7200', '-i', video_url, 
            '-ss', '7200', '-i', audio_url,
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
