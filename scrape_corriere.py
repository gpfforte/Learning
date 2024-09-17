from bs4 import BeautifulSoup
import requests
import csv
import sys
import os
from logging import DEBUG
from servizio import log_setup
from time import perf_counter

start = perf_counter()

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)

logger.info("Inizio")
PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


def raggruppa(soup_article, dettaglio):
    for single in soup_article.find_all("div", class_="content"):
        for p in single.find_all("p"):
            # print(p.text)
            dettaglio = f"{dettaglio} {p.text})"
    return dettaglio


i = 0


def main():
    global i
    source = requests.get("https://www.corriere.it/").text
    # soup = BeautifulSoup(source, 'lxml')
    soup = BeautifulSoup(source, features="lxml")
    # soup = BeautifulSoup(source, 'html')

    with open("scrape_corriere.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        csv_writer.writerow(["headline", "subheadline", "link", "dettaglio"])
        for article in soup.find_all("div", class_="media-news__content"):
            # print(article)
            dettaglio = ""
            link = ""
            try:
                i += 1
                headline = article.h4.a.text
                source_article = requests.get(article.h4.a["href"]).text
                soup_article = BeautifulSoup(source_article, features="lxml")
                dettaglio = raggruppa(soup_article, dettaglio)
                link = article.h1.a["href"]
            except:
                i += 1
            #     headline = article.h2.a.text
            #     source_article = requests.get(article.h2.a['href']).text
            #     soup_article = BeautifulSoup(source_article, features="lxml")
            #     dettaglio = raggruppa(soup_article, dettaglio)
            #     link = article.h2.a['href']
            subheadline = ""
            if i > 10:
                break
            csv_writer.writerow([headline, subheadline, link, dettaglio])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

end = perf_counter()

logger.info(f"Fine - Elapsed Time: {end - start}")
