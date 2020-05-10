#!/usr/bin/python3.8

import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import pandas
from tabula import read_pdf

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/tmp/", StaticFiles(directory="/tmp"), name="tmp")
origins = [
    "http://127.0.0.1",
    "http://pankgeorg.com",
    "https://pankgeorg.com",
    "http://www.pankgeorg.com",
    "https://www.pankgeorg.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
