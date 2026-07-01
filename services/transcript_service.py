import os
import re
import glob
import tempfile
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL


def extract_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/shorts/")[1].split("/")[0]

        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[1].split("/")[0]

    if parsed.hostname in ["youtu.be", "www.youtu.be"]:
        return parsed.path.lstrip("/").split("?")[0]

    match = re.search(r"([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None


def clean_vtt(text):
    lines = text.splitlines()
    cleaned = []
    previous_line = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("WEBVTT"):
            continue

        if "-->" in line:
            continue

        if line.isdigit():
            continue

        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\[.*?\]", "", line)
        line = re.sub(r"&amp;", "&", line)
        line = re.sub(r"&quot;", '"', line)
        line = re.sub(r"&#39;", "'", line)

        line = line.strip()

        if line and line != previous_line:
            cleaned.append(line)
            previous_line = line

    return " ".join(cleaned)


def get_transcript_from_api(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id,
        languages=[
            "en", "en-US", "en-GB",
            "hi", "hi-IN",
            "te", "ta", "kn", "ml"
        ]
    )

    return " ".join(
        item["text"].replace("\n", " ").strip()
        for item in transcript
        if item.get("text")
    )


def get_transcript_from_ytdlp(video_url):
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": [
                "en", "en.*",
                "hi", "hi.*",
                "te", "te.*",
                "ta", "ta.*"
            ],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        files = glob.glob(os.path.join(temp_dir, "*.vtt"))

        if not files:
            return None

        with open(files[0], "r", encoding="utf-8") as file:
            return clean_vtt(file.read())


def get_transcript(video_url):
    video_id = extract_video_id(video_url)

    if not video_id:
        return None, "Invalid YouTube URL."

    try:
        text = get_transcript_from_api(video_id)

        if text and len(text.strip()) > 50:
            return text.strip(), None

    except Exception:
        pass

    try:
        text = get_transcript_from_ytdlp(video_url)

        if text and len(text.strip()) > 50:
            return text.strip(), None

    except Exception as e:
        return None, (
            "YouTube blocked transcript access. "
            "Please paste transcript manually."
        )

    return None, "Could not extract transcript. Please paste transcript manually."