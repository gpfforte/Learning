from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import eyed3
from eyed3.id3 import (
    Tag,
    ID3_DEFAULT_VERSION,
    ID3_V2_3,
    ID3_V2_4,
    ID3_V1,
    ID3_V1_1,
    ID3_V1_0,
    ID3_V2,
    ID3_ANY_VERSION,
)
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2
from servizio import log_setup
from time import time

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

start = time()
logger.info("Inizio")
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
mp3_directory = os.path.join(dname, "archivio")
file_count = 0


def imposta_tags(file, artist, song):
    mp3_file_name = os.path.join(mp3_directory, file)
    # audio = EasyID3(mp3_file_name)
    audio = MP3(mp3_file_name, ID3=EasyID3)
    audio["artist"] = artist
    audio["title"] = song
    audio["tracknumber"] = "0"
    audio["album"] = "The Last Cop - Soundtrack"
    audio.save()
    print(audio)
    # print(EasyID3.valid_keys.keys())
    # audio.delete()
    # # mp3 = eyed3.load(mp3_file_name, tag_version=ID3_V1_0)
    # mp3 = eyed3.load(mp3_file_name, tag_version=ID3_ANY_VERSION)
    # mp3.initTag()
    # mp3.tag.song = song
    # mp3.tag.artist = artist
    # mp3.tag.title = song
    # mp3.tag.save()

    # file_name = os.path.join(mp3_directory, file)
    # # Create MP3File instance.
    # mp3 = MP3File(file_name)
    # mp3.set_version(VERSION_2)
    # mp3.genre = ""
    # mp3.track = 0
    # mp3.set_version(VERSION_BOTH)
    # mp3.song = song
    # mp3.artist = artist
    # mp3.album = ""
    # mp3.comment = ""
    # mp3.year = 2023

    # After the tags are edited, you must call the save method.


def ottieni_tags(file):
    file_name = os.path.join(mp3_directory, file)
    logger.info(file_name)
    mp3 = MP3File(file_name)
    mp3.set_version(VERSION_BOTH)
    tags = mp3.get_tags()
    print(tags)


def main():
    global file_count
    files = os.listdir(mp3_directory)
    files_mp3 = [f for f in files if f[-3:].upper() == ("MP3")]
    # print(files_mp3)
    for i in files_mp3:
        tags = i.split("-")
        artist = tags[0].strip()
        logger.info(f"Artist: {artist}")
        song = tags[1].strip()
        logger.info(f"Title: {song}")
        file_count += 1
        logger.info(i)
        imposta_tags(i, artist, song)
        # ottieni_tags(i)
        # i.copy(copy_directory)
    logger.info(f"Ci sono {file_count} mp3")


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

"""
Allowed tags:

    - artist;
    - album;
    - song;
    - track;
    - comment;
    - year;
    - genre;
    - band (version 2.x);
    - composer (version 2.x);
    - copyright (version 2.x);
    - url (version 2.x);
    - publisher (version 2.x).
"""
