import os
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = os.getenv("DATABASE_URI")
if not DATABASE_URI:
    print("Failed to find DATABASE_URI env variable")
Base = declarative_base()
NOW = lambda: datetime.now(timezone.utc)

engine = create_engine(DATABASE_URI, echo=False)
connection = engine.connect()
connection.execute("CREATE SCHEMA IF NOT EXISTS weather_station")
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
session = SessionFactory()


class Reading(Base):
    __tablename__ = "reading"
    __table_args__ = {"schema": "weather_station"}
    reading_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=NOW)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    gas_resistance = Column(Float)
    weather_station = Column(String)


Base.metadata.create_all(engine, checkfirst=True)
