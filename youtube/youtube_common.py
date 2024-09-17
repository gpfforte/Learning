from servizio import log_setup
import pafy
from pydub import AudioSegment
import logging
import sys
import os

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)


def scarica_audio(video, change_name=False, title="titolo"):
    """Scarica il miglior audio e lo converte in mp3 a partire da qualunque formato (sempre che lo gestisca...)"""
    for i in video.audiostreams:
        logger.info(
            f"bitrate = {i.bitrate}, dimensione = {i.get_filesize()/1024/1024:0.2f}MB, estensione = {i.extension}, filename = {i.filename}")
    bestaudio = video.getbestaudio()
    title_with_extension = f"{title}.{bestaudio.extension}"
    if change_name:
        bestaudio.download(filepath=title_with_extension)
    else:
        bestaudio.download(filepath=dname)

    logger.info("Fine Download")
    #print("Fine Download")
    file_scaricato = bestaudio.filename if not change_name else title_with_extension
    logger.info("Inizio Estrazione: "+bestaudio.filename)
    #print("Inizio Estrazione: "+bestaudio.filename)
    song = AudioSegment.from_file(
        file_scaricato, format=bestaudio.extension)
    logger.info("Fine Estrazione")
    #print("Fine Estrazione")

    filename_da_salvare = bestaudio.title + \
        ".mp3" if not change_name else title+".mp3"
    logger.info("Inizio Conversione: "+filename_da_salvare)
    #print("Inizio Conversione: "+filename_da_salvare)
    song.export(filename_da_salvare, format="mp3")
    logger.info("Fine Conversione")
    # print("Fine Conversione")
    if bestaudio.extension != "mp3":
        os.remove(file_scaricato)
        logger.info("Cancellato file: "+file_scaricato)
        #print("Cancellato file: "+file_scaricato)
    return filename_da_salvare


def scarica_video(video):
    """Scarica il miglior video disponibile"""
    for s in video.streams:
        logger.info(
            f"titolo = {s.title}, resolution = {s.resolution}, estensione = {s.extension}, dimensione = {s.get_filesize()/1024/1024:0.2f}MB")
    bestvideo = video.getbest()
    bestvideo.download(filepath=dname)


def converti_file(filename):
    """Converte un file di qualsiasi formato in mp3"""
    title, extension = filename.split(".")
    song = AudioSegment.from_file(
        filename, format=extension)
    filename_da_salvare = title+".mp3"
    logger.info(dname + "/" + filename_da_salvare)
    song.export(filename_da_salvare, format="mp3")
