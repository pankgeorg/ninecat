U = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}&units=metric"

import datetime
import json
import logging
from time import sleep
from typing import List, Tuple

import requests

from models.Weather import OpenWeatherResultOrm
from settings import LOG_FILE
from settings import OPENWEATHERKEY as K

log = logging.getLogger(LOG_FILE)
log.info(f"{__name__} Loading @{datetime.datetime.now()}")


Location = Tuple[float, float]


def get_locations() -> List[Location]:
    locations = [
        (38.004048, 23.7812553),  # Aiolou 12
        (37.9980414, 23.7832123),  # Dimokratias 35
        (37.9775323, 23.7293643),  # Lozenge
    ]
    return [(lon, lat) for (lat, lon) in locations]


def get_location(lon: float, lat: float):
    url = U.format(lat=lat, lon=lon, key=K)
    result = requests.get(url)
    code = result.status_code
    s_lon = str(lon)
    s_lat = str(lat)
    info = ""
    data = {}
    if result.ok:
        data = result.json()
    wOrm = OpenWeatherResultOrm(lon=s_lon, lat=s_lat, info=info, data=data, code=code)
    return wOrm


def run():
    locations = get_locations()
    for (lon, lat) in locations:
        log.info(f"{__name__} crawling ({lon}, {lat})")
        wOrm = get_location(lon, lat)
        wOrm.save(commit=False)
        sleep(2)
    OpenWeatherResultOrm.session.commit()
