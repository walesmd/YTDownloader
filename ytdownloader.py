#!/usr/bin/env python

import os
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed

DEST_DIR = "./downloads"
MAX_WORKERS = 4

class ThreadPoolManager:
    """
    Thread pool manager for concurrent YouTube downloads.
    """

    def __init__(self, max_workers: int = MAX_WORKERS):
        self.executor = ThreadPoolExecutor(max_workers = max_workers)
        self.futures = []

    def add_task(self, url: str, output_path: str = DEST_DIR):
        """Submit a video download task to the pool."""
        future = self.executor.submit(download_video, url, output_path)
        self.futures.append(future)

    def wait_for_completion(self):
        """Wait for all tasks to complete and return results."""
        results = []
        for future in as_completed(self.futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"url": None, "error": str(e)})

        return results

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

    downloader = ThreadPoolManager(max_workers = MAX_WORKERS)

    urls = [
        "https://www.youtube.com/watch?v=EeJ8n5PxFGE",
        "https://www.youtube.com/watch?v=2lAe1cqCOXo"
    ]

    for url in urls:
        downloader.add_task(url)

    all_results = downloader.wait_for_completion()
    print("\nSummary of downloads:")
    for result in all_results:
        print(result)