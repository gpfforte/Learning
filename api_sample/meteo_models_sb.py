import datetime as dt
import os
from logging import DEBUG

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy.schema import UniqueConstraint

from servizio import log_setup
from servizio.supabase_db import engine_sb, session_sb

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)


Base = declarative_base()


class City(Base):
    __tablename__ = "meteo.city"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)
    iso2 = Column(String)
    meteodata = relationship("MeteoData", back_populates="city")

    def __str__(self):
        return f"{self.name}"


class MeteoData(Base):
    __tablename__ = "meteo.meteo_data"
    id = Column(Integer, primary_key=True)
    datetime_created = Column(DateTime, default=dt.datetime.now)
    datetime_sunrise = Column(DateTime)
    datetime_sunset = Column(DateTime)
    temperature = Column(Float)  # Celsius
    pressure = Column(Float)  # hPa
    humidity = Column(Float)  # %
    wind_speed = Column(Float)  # Km/h
    wind_dir = Column(Integer)  # °
    weather_description = Column(String)
    city_id = Column(Integer, ForeignKey("meteo.city.id"))
    city = relationship("City", back_populates="meteodata")

    def __str__(self):
        return f"(Date {self.datetime_created} - Meteo for {self.city})"


def populate_cities():
    cities_dict = {
        "Bordighera": {"lat": 43.7855, "long": 7.6585, "country_iso2": "IT"},
        "Imperia": {"lat": 43.8843, "long": 8.0233, "country_iso2": "IT"},
        "Milano": {"lat": 45.466944, "long": 9.19, "country_iso2": "IT"},
        "Berlino": {"lat": 52.516667, "long": 13.383333, "country_iso2": "DE"},
        "Corvara in Badia": {"lat": 46.55037, "long": 11.87342, "country_iso2": "IT"},
    }
    cities = []
    for key, value in cities_dict.items():
        with session_sb:
            city = City(
                name=key,
                lat=value["lat"],
                long=value["long"],
                iso2=value["country_iso2"],
            )
            cities.append(city)
            session_sb.add_all(cities)
            session_sb.commit()
        # print(key, value)


def main():
    populate_cities()
    Base.metadata.create_all(engine_sb)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(e, exc_info=True)
