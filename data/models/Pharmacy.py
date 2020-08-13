from typing import Optional

from models.BaseOrm import BaseOrm
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class PharmacyOrm(BaseOrm):
    __tablename__ = "pharmacy"
    __table_args__ = {"schema": "fsa"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    fsa_id = Column(String)
    name = Column(String)
    address = Column(String)
    area = Column(String)
    tel = Column(String)


class DutyOrm(BaseOrm):
    __tablename__ = "duty"
    __table_args__ = {"schema": "fsa"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    fsa_id = Column(String)
    name = Column(String)
    area = Column(String)
    time = Column(String)
    date = Column(String)


class Duty(BaseModel):
    fsa_id: str
    name: str
    area: str
    time: str
    date: str

    class Config:
        orm_mode = True


class Pharmacy(BaseModel):
    fsa_id: str
    name: str
    address: Optional[str]
    area: Optional[str]
    tel: Optional[str]

    class Config:
        orm_mode = True
