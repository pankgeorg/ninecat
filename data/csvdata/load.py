from io import BytesIO

import pandas
from google.cloud import storage

from database import engine

client = storage.Client()


def cities500():

    bucket = client.get_bucket("silentech.gr")
    blob = bucket.get_blob("csvs/cities500.txt")
    file = BytesIO(blob.download_as_bytes())
    names = [
        "geonameid",
        "name",
        "asciiname",
        "alternatenames",
        "latitude",
        "longitude",
        "feature class",
        "feature code",
        "country code",
        "cc2",
        "admin1 code",
        "admin2 code",
        "admin3 code",
        "admin4 code",
        "population",
        "elevation",
        "dem",
        "timezone",
        "modification date",
    ]
    cities = pandas.read_csv(file, names=names, delimiter="\t", low_memory=False)
    cities.to_sql(
        "geonames_cities500",
        engine,
        schema="places",
        if_exists="replace",
        method="multi",
    )


def run():
    cities500()
