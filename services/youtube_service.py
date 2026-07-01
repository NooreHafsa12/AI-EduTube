import re
import yt_dlp


def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_video_info(url):
    try:
        options = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title", "YouTube Video"),
            "channel": info.get("uploader", "Unknown Channel"),
            "duration": info.get("duration_string", "N/A"),
            "thumbnail": info.get("thumbnail", ""),
            "url": url
        }

    except Exception:
        video_id = extract_video_id(url)

        return {
            "title": "YouTube Video",
            "channel": "Unknown Channel",
            "duration": "N/A",
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else "",
            "url": url
        }