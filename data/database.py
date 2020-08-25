import logging
from functools import partial
from json import dumps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from settings import DATABASE_URI, ENVIRONMENT

log = logging.getLogger(__name__)
engine = create_engine(
    DATABASE_URI,
    echo=(True if ENVIRONMENT != "production" else False),
    json_serializer=partial(
        dumps, ensure_ascii=False
    ),  # https://stackoverflow.com/questions/58444110/postgresql-json-column-not-saving-utf-8-character
)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
session = SessionFactory()


def get_connection():
    try:
        connection = engine.connect()
        log.info(f"Connection successful at: {DATABASE_URI}")
        return connection
    except Exception as e:
        log.critical(f"Cannot connect to database, failed with exception {str(e)}")
        return None


def init_db():
    with get_connection() as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS fsa;")
        con.execute("CREATE SCHEMA IF NOT EXISTS weather;")
        con.execute("CREATE SCHEMA IF NOT EXISTS places;")
    Base.metadata.create_all(engine, checkfirst=True)
