U = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}&units=metric"
URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"

import datetime
import json
import logging
import time
from time import sleep
from typing import List, Tuple

import requests
from pandas import read_sql_query

from database import engine
from models.Weather import OpenWeatherResultOrm
from settings import LOG_FILE
from settings import OPENWEATHERKEY as K

log = logging.getLogger(LOG_FILE)
log.info(f"{__name__} Loading @{datetime.datetime.now()}")

Location = Tuple[float, float]  # lon, lat γιατί έτσι


def greek_cities(count=2000):
    locations = read_sql_query(
        f"""
select latitude, longitude, name
from places.geonames_cities500
where "country code" = 'GR'
order by population desc
limit {count}""",
        engine,
    )
    return [(lon, lat, name) for (i, (lat, lon, name)) in locations.iterrows()]


def get_location(lon: float, lat: float, endpoint_type="onecall", info=""):
    if endpoint_type == "onecall":
        url = U.format(lat=lat, lon=lon, key=K)
    if endpoint_type == "weather":
        url = URL_CURRENT.format(lat=lat, lon=lon, key=K)
    else:
        raise Exception("Invalid endpoint type")
    result = requests.get(url)
    code = result.status_code
    s_lon = str(lon)
    s_lat = str(lat)
    info = f"{endpoint_type} - {info}"
    data = {}
    if result.ok:
        data = result.json()
    wOrm = OpenWeatherResultOrm(
        lon=s_lon, lat=s_lat, info=info, data=data, code=code, url=url
    )
    return wOrm


def greek_cities_current_weather(count=1500):
    for lon, lat, name in greek_cities(count):
        log.info(f"{__name__} crawling {name}@({lon}, {lat})")
        datum = get_location(lon, lat, "weather", name)
        datum.save(commit=True)
        sleep(1.1)


def run(count):
    greek_cities_current_weather(count)
