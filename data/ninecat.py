from typing import Optional
import logging
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
def nothing():
    pass


if __name__ == "__main__":
    app()
