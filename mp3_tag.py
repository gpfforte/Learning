from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
from servizio import log_setup

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)


# Create MP3File instance.
mp3 = MP3File("Frankie Goes To Hollywood - The Power Of Love.mp3")
mp3.set_version(VERSION_BOTH)

mp3.album = "Not Specified"
mp3.song = "Take Me To Church"
mp3.artist = "Hozier"
mp3.track = "1"
mp3.comment = "Commento"
mp3.year = "2000"

# After the tags are edited, you must call the save method.
mp3.save()

mp3.set_version(VERSION_2)

mp3.genre = "Folk"
mp3.band = "Band"
mp3.composer = "Composer"
mp3.copyright = "Copyright"
mp3.url = "www.youtube.com"
mp3.publisher = "Publisher"

# After the tags are edited, you must call the save method.
mp3.save()

mp3.set_version(VERSION_BOTH)

tags = mp3.get_tags()
print(tags)

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
