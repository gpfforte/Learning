import datetime as dt
import json
import os
import sys

import pytz
import requests
from meteo_models_sb import City, MeteoData, engine_sb, session_sb

from servizio import log_setup

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
print(PROVA)
# cities_dict = {"Bordighera": {"lat": 43.7855, "lon": 7.6585, "country_iso2": "IT"},
#                "Imperia": {"lat": 43.8843, "lon": 8.0233, "country_iso2": "IT"},
#                "Milano": {"lat": 45.466944, "lon": 9.19, "country_iso2": "IT"},
#                "Berlino": {"lat": 52.516667, "lon": 13.383333, "country_iso2": "DE"},
#                "Corvara in Badia": {"lat": 46.55037, "lon": 11.87342, "country_iso2": "IT"}, }

cities_list = [
    ["Bordighera", "IT"],
    ["Imperia", "IT"],
    ["Milano", "IT"],
    ["Berlino", "DE"],
    ["Corvara in Badia", "IT"],
]

# lat = 43.7855
# lon = 7.6585
api_key = os.environ.get("API_KEY_OPENWEATHERMAP")

tz = pytz.timezone("Europe/Rome")


def geocode(city):
    # http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}

    api_request = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city[0]},{city[1]}&limit=5&appid={api_key}"
    )
    api = json.loads(api_request.content)
    # print(api)
    return api


def main():
    # f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"

    for city in cities_list:
        print()
        print(city)
        api = geocode(city)
        print(f"Numero risultati trovati per {city}: {len(api)}")

        if api:
            if len(api) > 1:
                if "state" in api[0]:
                    print(
                        f"Dati per la prima occorrenza - {api[0]['name']} - {api[0]['country']} - {api[0]['state']}"
                    )
                else:
                    print(
                        f"Dati per la prima occorrenza - {api[0]['name']} - {api[0]['country']}"
                    )
            lat = api[0]["lat"]
            lon = api[0]["lon"]
            api_request = requests.get(
                f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            )
            api = json.loads(api_request.content)
            # Time is the number of seconds from EPOCH (1 Gennaio 1970)
            utc_time_current = dt.datetime.utcfromtimestamp(
                api["current"]["dt"])

            local_time_current = (
                pytz.utc.localize(utc_time_current, is_dst=None)
                .astimezone(tz)
                .strftime("%Y-%m-%d %H:%M:%S")
            )

            utc_time_sunrise = dt.datetime.utcfromtimestamp(
                api["current"]["sunrise"])
            local_time_sunrise = (
                pytz.utc.localize(utc_time_sunrise, is_dst=None)
                .astimezone(tz)
                .strftime("%Y-%m-%d %H:%M:%S")
            )

            utc_time_sunset = dt.datetime.utcfromtimestamp(
                api["current"]["sunset"])
            local_time_sunset = (
                pytz.utc.localize(utc_time_sunset, is_dst=None)
                .astimezone(tz)
                .strftime("%Y-%m-%d %H:%M:%S")
            )

            print(f"Latitudine: \t {lat}")
            print(f"Longitudine: \t {lon}")

            print(
                f"Current Time: \t {local_time_current}", f" (utc) {utc_time_current}"
            )
            print(f"Surise Time: \t {local_time_sunrise}",
                  f" (utc) {utc_time_sunrise}")
            print(f"Sunset Time: \t {local_time_sunset}",
                  f" (utc) {utc_time_sunset}")
            print(f"Temperature: \t {api['current']['temp']} °C")
            print(f"Pressure: \t {api['current']['pressure']} hPa")
            print(f"Humidity: \t {api['current']['humidity']} %")
            print(f"Wind Speed: \t {api['current']['wind_speed']} Km/h")
            print(f"Wind Dir: \t {api['current']['wind_deg']} °")
            print(
                f"Description: \t {api['current']['weather'][0]['description'].title()}"
            )
            print()
            # print(api['current'])


logger.info("Inizio")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)

logger.info("Fine")
