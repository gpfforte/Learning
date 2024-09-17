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
    for single in soup_article.find_all("div", class_="news-single-content"):
        for p in single.find_all("p"):
            # print(p.text)
            dettaglio = f"{dettaglio} {p.text})"
    return dettaglio


def main():
    source = requests.get("https://www.sanremonews.it/").text

    # soup = BeautifulSoup(source, 'lxml')
    soup = BeautifulSoup(source, features="lxml")
    # soup = BeautifulSoup(source, 'html')

    # logger.debug(soup.prettify())
    # TODO SAREBBERO DA PULIRE I CARATTERI SPORCHI CHE POI VANNO NEL FILE E NON SONO
    # INTERPRETATI CORRETTAMENTE DAL PARSER CSV ######################
    with open("scrape_sanremonews.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        csv_writer.writerow(["headline", "subheadline", "link", "dettaglio"])
        for article in soup.find_all("div", class_="news-list-item"):
            # print(article)
            dettaglio = ""
            try:
                headline = article.h1.a.text
                source_article = requests.get(article.h1.a["href"]).text
                soup_article = BeautifulSoup(source_article, features="lxml")
                dettaglio = raggruppa(soup_article, dettaglio)
                # for single in soup_article.find_all('div', class_='news-single-content'):
                #     for p in single.find_all('p'):
                #         # print(p.text)
                #         dettaglio = f'{dettaglio} {p.text})'
                # logger.debug(soup_article.prettify())
                link = article.h1.a["href"]
            except:
                headline = article.h2.a.text
                source_article = requests.get(article.h2.a["href"]).text
                soup_article = BeautifulSoup(source_article, features="lxml")
                dettaglio = raggruppa(soup_article, dettaglio)
                # for single in soup_article.find_all('div', class_='news-single-content'):
                #     for p in single.find_all('p'):
                #         # print(p.text)
                #         dettaglio = f'{dettaglio} {p.text})'

                # logger.debug(soup_article.prettify())
                link = article.h2.a["href"]

            subheadline = article.p.text

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
