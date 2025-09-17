#!/usr/bin/env python

import yt_dlp
import os

DEST_DIR = "./downloads"

def download_video(url: str, output_path: str = DEST_DIR):
    try:
        metadata = {}
        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download = True)

            metadata["title"] = info.get("title")
            metadata["author"] = info.get("uploader")
            metadata["author_url"] = info.get("uploader_url")
            metadata["duration_seconds"] = info.get("duration")
            metadata["video_url"] = url

            print(f"Download: {metadata['title']}")

            return metadata

    except Exception as e:
        print(f"Error downloading video: {e}")
        return {"url": url, "error": str(e)}


if __name__ == "__main__":
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)


    urls = [
        "https://www.youtube.com/watch?v=EeJ8n5PxFGE",
        "https://www.youtube.com/watch?v=2lAe1cqCOXo"
    ]

    video_url = urls[0]
    download_video(video_url)