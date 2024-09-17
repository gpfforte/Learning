from time import time
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor, as_completed
from servizio import log_setup
import pafy
from pydub import AudioSegment
import logging
import sys
import os
import shutil
from youtube_common import scarica_audio, scarica_video, converti_file

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

playlist_link = "https://www.youtube.com/watch?v=ADVCHpdmA5M&list=PL5--8gKSku15uYCnmxWPO17Dq6hVabAB4"

start = time()
logger.info("Inizio")
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# print(video_links)


def main():
    video_links = list(Playlist(playlist_link).video_urls)
    logger.info(video_links)
    for idx, url in enumerate(video_links[:]):
        change_name = False
        title = YouTube(url).title
        to_check = '/|?_":'
        for char in to_check:
            if char in title:
                change_name = True
                logger.info(f"Traccia {idx} titolo {title}")
                logger.info(f"Carttere: {char} in titolo: {title}")
                title = title.replace(char, "")
        logger.info(change_name)
        logger.info(url)
        video = pafy.new(url)
        logger.info(title)
        filename_da_salvare = scarica_audio(video, change_name, title)
        shutil.move(filename_da_salvare, f"archivio/{filename_da_salvare}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

logger.info("Fine")

logger.info(f"Time taken: {time() - start}")
