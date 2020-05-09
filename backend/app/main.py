#!/usr/bin/python3.8

import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile
from tabula import read_pdf

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/daduploadfile/")
def handler(upload_file: UploadFile = File(...)):
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
        xl_table = read_pdf(tmp_path, pages=1)
        xl_table[0].to_excel("test_this.xlsx")
    finally:
        upload_file.file.close()

    return {"filename": upload_file.filename, "tmp": tmp_path}
