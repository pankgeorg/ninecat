from models.BaseOrm import BaseOrm
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class PlaceSearch(BaseOrm):
    """Enter text to find place id"""

    __tablename__ = "place_text_search"
    __table_args__ = {"schema": "places"}
    text_input = Column(String)
    input_type = Column(String, default="textquery")
    locationbias = Column(
        String, default="circle:1000000@37.8945342,23.7307223"
    )  # 1.000km around Athens, Greece
    priority = Column(Integer, default=0)
    data = Column(JSON)
    places = relationship("PlaceDetail", back_populates="search")
    source_entity_id = Column(String)  # Use this in ETL


class PlaceDetail(BaseOrm):
    """Enter Id to fill with data"""

    __tablename__ = "place_id_detail"
    __table_args__ = {"schema": "places"}
    gmaps_id = Column(String)
    priority = Column(Integer, default=0)
    search_id = Column(Integer, ForeignKey(PlaceSearch.id))
    search = relationship("PlaceSearch", back_populates="places")
    data = Column(JSON)
