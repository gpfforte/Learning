from time import time
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor, as_completed
from servizio import log_setup
from pydub import AudioSegment
import os
"""

"""
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
playlist_link = "https://www.youtube.com/playlist?list=PLbtjwUbdf_nK-LvL_wuq5Ji2ML2-W9kip"
start = time()
video_links = Playlist(playlist_link).video_urls

print(video_links)


def get_video_title(link):
    title = YouTube(link).title
    return title


def get_title_parallel():
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in video_links:
            processes.append(executor.submit(get_video_title, url))

    video_titles = []
    for task in as_completed(processes):
        video_titles.append(task.result())
        print(task.result())


def main():
    for idx, link in enumerate(video_links):
        logger.info(f"[{idx}] - {YouTube(link).title}")
    # get_title_parallel()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)

logger.info("Fine")

logger.info(f'Time taken: {time() - start}')
