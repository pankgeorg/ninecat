import logging
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer

from database import session
from models import Base
from settings import LOG_FILE
log = logging.getLogger(LOG_FILE)

NOW = lambda: datetime.now(timezone.utc)


class BaseOrm(Base):
    "Any one of our models will inherit the below"
    __abstract__ = True  # Don't instanciate this!
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=NOW)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    session = session

    def save(self, commit=True):
        "Saves an object"
        self.session.add(self)
        if commit:
            try:
                self.session.commit()
            except Exception as e:
                log.error(str(e))
            finally:
                self.session.close()

    @classmethod
    def get_by_id(cls, id):
        "Return an object by id"
        return cls.session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_attribute(cls, **kwargs):
        "Return all object with specific arguments"
        return cls.session.query(cls).filter(**kwargs).all()
