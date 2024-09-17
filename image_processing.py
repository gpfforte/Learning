import os
from servizio import log_setup
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import shutil
# TODO Rimane da verificare di non cercare di aprire una directory e vedere
#  come chiudere il file dell'immagine se si volesse cnacellare
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

logger.info("Inizio")


def main():
    os.chdir("Images")
    cwd = os.getcwd()
    print("os.listdir():", os.listdir())
    for item in os.listdir():
        print(item)
        print("########################################")
        image = Image.open(item)
        exifdata = image.getexif()
        # iterating over all EXIF data fields
        for tag_id in exifdata:
            if tag_id == 36867:  # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decode bytes
                if isinstance(data, bytes):
                    try:
                        data = data.decode()
                    except:
                        data = "No Decode"
                date_time = datetime.strptime(data, "%Y:%m:%d %H:%M:%S")
                # print(date_time, date_time.year, date_time.month)
                # print(f'{date_time.month:02}')
                mese = f'{date_time.month:02}'
                anno = f'{date_time.year:04}'
                # print(mese)
                # print(f"{tag_id:25}: {tag:25}: {data}")
                path_img = anno+"\\"+mese
                path_img_completo = cwd+"\\"+path_img
                if not os.path.exists(path_img_completo):
                    os.makedirs(path_img_completo)
                origine = cwd+"\\"+item
                destinazione = path_img_completo+"\\"+item
                print(origine, destinazione)
                shutil.copy(origine, destinazione)

        # print("size of", item, "is", os.path.getsize(item))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)

logger.info("Fine")
