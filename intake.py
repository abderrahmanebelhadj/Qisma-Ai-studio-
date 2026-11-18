import os
import urllib.request
from urllib.parse import urlparse

def collect_video():
    print("QISMA AI - VIDEO COLLECTOR")

    url = os.environ.get("QISMA_VIDEO_URL", "").strip()

    if not url:
        print("Waiting for an authorized video URL.")
        return

    parsed = urlparse(url)

    if parsed.scheme != "https":
        print("Error: HTTPS link required.")
        return

    print("Checking video source...")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "QismaAI/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if not (
                content_type.startswith("video/")
                or "application/octet-stream" in content_type
            ):
                print("Error: This is not a direct video file.")
                return

            total = 0
            max_size = 500 * 1024 * 1024

            with open("source_video.mp4", "wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)

                    if not chunk:
                        break

                    total += len(chunk)

                    if total > max_size:
                        raise ValueError("Video exceeds 500 MB")

                    file.write(chunk)

        print("Video received successfully!")
        print("Size:", round(total / 1024 / 1024, 2), "MB")

    except Exception as error:
        print("Collection failed:", error)

if name == "main":
    collect_video()
