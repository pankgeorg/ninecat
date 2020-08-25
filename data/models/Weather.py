from models.BaseOrm import BaseOrm
from pydantic import BaseModel
from sqlalchemy import JSON, Column, Integer, String

U = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}"


class OpenWeatherResultOrm(BaseOrm):
    __tablename__ = "onecall_result"
    __table_args__ = {"schema": "weather"}
    lon = Column(String)
    lat = Column(String)
    url = Column(String)
    info = Column(String)
    code = Column(Integer)
    data = Column(JSON)
