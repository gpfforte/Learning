from servizio import log_setup
import pafy
from pydub import AudioSegment
import logging
import sys
import os
from youtube_common import scarica_audio, scarica_video, converti_file
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

logger.info("Inizio")

# Questo programma permette di scaricare da youtube video e/o audio a partire dallo url
# Scarica il miglior video ed il miglior audio
# Sono definite 2 funzioni apposite al quale passare in input il parametro video
# E' anche presente una funzione di conversione audio che può trasformare da qualsiasi formato a mp3


def main():
    # url = "https://www.youtube.com/watch?v=PVjiKRfKpPI"
    url = "https://www.youtube.com/watch?v=NyoTvgPn0rU&list=PLbtjwUbdf_nK-LvL_wuq5Ji2ML2-W9kip&index=1"
    logger.info(url)
    video = pafy.new(url)
    # scarica_video(video)
    scarica_audio(video)
    # converti_file("Hozier - Take Me To Church (Official Video).mp3")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)

logger.info("Fine")
