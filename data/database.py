import logging

from models import Base
from settings import DATABASE_URI, ENVIRONMENT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)
engine = create_engine(
    DATABASE_URI, echo=(True if ENVIRONMENT != "production" else False)
)
SessionFactory = sessionmaker(bind=engine)
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
    Base.metadata.create_all(engine, checkfirst=True)
