#!/usr/bin/python3.8

import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import pandas
from tabula import read_pdf

from app.database import Reading, session
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/tmp/", StaticFiles(directory="/tmp"), name="tmp")


@app.get("/")
def read_root():
    return {"Hello": "World"}


#  OK that's not rest/http compliant
@app.get("/station-readings")
def read_station_readings(
    temp: float,
    gasr: float,
    pres: float,
    humd: float,
    s: str,
    gust: float,
    wind: float,
    wndc: int,
    degr: int,
    watr: int,
    now: float,
    prev: float,
):
    reading = Reading(
        temperature=temp,
        gas_resistance=gasr,
        humidity=humd,
        pressure=pres,
        weather_station=s,
        gust=gust,
        wind=wind,
        wind_count=wndc,
        wind_direction=degr,
        water_count=watr,
        now=now,
        prev=prev,
    )
    session.add(reading)
    session.commit()
    session.close()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


def getDadValues(df: pandas.DataFrame):
    C = "Unnamed: 0"
    C2 = "Unnamed: 1"

    return [
        [
            "date",
            "Price_in",
            "m3",
            "m3",
            "m3",
            "m3",
            "m3",
            "mt",
            "mt",
            "mt",
            "mt",
            "mt",
        ],
        [
            "date",
            "euro/m3",
            "UNL100",
            "UNL95",
            "UNL98",
            "AGO",
            "HGO",
            "KERO",
            "FO1I",
            "FO3I",
            "FO3L",
            "BITUMEN",
        ],
        [
            "Not Parsed",
            "HP",
            df[C].loc[10],
            df[C].loc[7],
            df[C].loc[9],
            df[C].loc[14],
            df[C].loc[17],
            df[C2].loc[20],
            df[C2].loc[26],
            df[C2].loc[27],
            "?",
            df[C2].loc[29],
        ],
    ]


@app.post("/daduploadfile/")
def handler(file: UploadFile = File(...)):
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpXl:
            xl_table = read_pdf(tmp_path, pages=1)
            xl_table[0].to_excel(tmpXl)
            data = getDadValues(xl_table[0])
    finally:
        file.file.close()

    return {
        "filename": file.filename,
        "pdfDownload": tmp.name,
        "excelDownload": tmpXl.name,
        "table": data,
        "data": xl_table[0].to_json(orient="records"),
    }
