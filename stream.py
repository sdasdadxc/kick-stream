import subprocess
import yt_dlp
import time

YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=Oqr0muaqH0c"
KICK_SERVER = "rtmps://fa723fc1b171.global-contribute.live-video.net/app/sk_us-west-2_ZPLESAknon8e_gjd2fxY128MUmSMT6j4BWavsmbTnK4"

while True:
    try:
        print("⚡ Extracting links and starting stream...")
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'quiet': True,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_VIDEO_URL, download=False)
            video_url = info['requested_formats'][0]['url']
            audio_url = info['requested_formats'][1]['url']

        print("🚀 Stream is LIVE now on Kick (Skipping first 2 hours)...")
        
        # التعديل هنا: ضفنا '-ss', '7200' قبل الإنبرت (-i) لكل من الفيديو والأوديو عشان يبدأ من الساعة الثالثة بالظبط
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
