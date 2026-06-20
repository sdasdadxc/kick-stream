import subprocess
import time

YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=Oqr0muaqH0c"
KICK_SERVER = "rtmps://fa723fc1b171.global-contribute.live-video.net/app/sk_us-west-2_MF3RDcWvwV0L_KSgTiQA4tCrDk7CdVqDPNy7ntSWIRX"

while True:
    try:
        print("🚀 Starting direct FFmpeg stream to bypass YouTube n-challenge...")
        
        # هنا بنخلي FFmpeg يسحب مباشرة باستخدام الكوكيز والـ User-Agent كأنه متصفح بدون الاعتماد الكامل على فك تشفير المتاح في yt-dlp
        ffmpeg_cmd = [
            'ffmpeg', '-re',
            '-cookies', 'cookies.txt',
            '-user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-ss', '7200', # سكايب أول ساعتين
            '-i', YOUTUBE_VIDEO_URL,
            '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'ultrafast',
            '-pix_fmt', 'yuv420p', '-g', '60', '-keyint_min', '60', '-sc_threshold', '0',
            '-b:v', '3000k', '-maxrate', '3000k', '-bufsize', '6000k',
            '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2',
            '-f', 'flv', KICK_SERVER
        ]
        
        print("📺 Stream is transferring to Kick now...")
        subprocess.run(ffmpeg_cmd)
        
        print("⚠️ Stream finished or disconnected. Reconnecting in 5 seconds...")
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Critical Error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
