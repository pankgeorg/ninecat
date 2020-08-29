"""This is the catalog of the services provided in this module"""
import logging
from typing import Optional

import typer
from settings import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE, format="%(asctime)s %(levelname)s %(threadName)-10s %(message)s"
)
log = logging.getLogger(LOG_FILE)

app = typer.Typer()


@app.command()
def update_fsa(N: Optional[str] = None):
    log.info("Update start")
    from fsa.crawler import run_with_db

    run_with_db(N)
    log.info("Job Finished")


@app.command()
def update_weather(cities_count: Optional[int] = 1500):
    log.info("getting greek weather")
    from weather.crawler import greek_cities_current_weather as run

    run(cities_count)
    log.info("weather job finished")


@app.command()
def process_place():
    log.info("Trying to do process a place")
    import places.crawler as pc

    pc.place_search_fill_data()
    pc.create_place_detail()
    pc.place_detail_fill_data()

    log.info("this may have suceeded, also maybe not")


@app.command()
def load_csv():
    from csvdata.load import run

    run()


if __name__ == "__main__":
    app()
