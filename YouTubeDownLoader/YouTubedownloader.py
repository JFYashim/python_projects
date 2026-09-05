import os
import sys
import yt_dlp

# Helper function to locate ffmpeg inside the packaged app
def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS  # PyInstaller temporary folder
    return "."

def download_youtube_video(url, output_path="."):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ffmpeg_location': get_ffmpeg_path(), # Tells yt-dlp where ffmpeg is!
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching video information for: {url}")
            ydl.download([url])
            print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube Video URL: ").strip()
    download_youtube_video(video_url)
