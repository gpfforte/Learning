import requests
import json
import datetime as dt
import pytz
import sys
import os
from servizio import log_setup
import geopandas as gpd
import pandas as pd

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

cities_list = ["Bordighera", "Imperia", "Milano", "Berlin", "Corvara in Badia"]
cities_dict = {"city": cities_list}

# lat = 43.7855
# lon = 7.6585
api_key = os.environ.get("API_KEY_OPENWEATHERMAP")

tz = pytz.timezone("Europe/Rome")


def main():
    df_cities = pd.DataFrame.from_dict(cities_dict)
    gdf_cities = gpd.tools.geocode(df_cities["city"])
    print(df_cities)
    print(gdf_cities)
    gdf_cities["lon"] = gdf_cities["geometry"].x
    gdf_cities["lat"] = gdf_cities["geometry"].y
    gdf_cities = pd.concat([df_cities, gdf_cities], axis=1)
    # f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"

    for idx, city in gdf_cities.iterrows():
        print()
        print(city)
        lat, lon = city["lat"], city["lon"]

        api_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        api = json.loads(api_request.content)
        # Time is the number of seconds from EPOCH (1 Gennaio 1970)
        utc_time_current = dt.datetime.utcfromtimestamp(api["current"]["dt"])

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

        print(f"Current Time: \t {local_time_current}",
              f" (utc) {utc_time_current}")
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
            f"Description: \t {api['current']['weather'][0]['description'].title()}")
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
