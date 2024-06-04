from aerial_photography.database.base_class import Base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    ARRAY,
    Integer,
    DateTime,
    ForeignKey, String
)
from sqlalchemy.orm import relationship


class PolygonsToSearchFor(Base):
    __tablename__ = "polygons_to_search_for"

    id = Column('id', Integer, primary_key=True)
    owner = Column('owner', Integer, ForeignKey("users.id"))
    owner_relationship = relationship("Users", back_populates="polygons_to_search_for_relationship", lazy='joined')

    name = Column("name", String)
    footprint = Column('footprint', Geometry('POLYGON'))  # Координаты полигона, в котором будут запрашиваться снимки
    start_time = Column("start_time", DateTime(timezone=True))
    end_time = Column("end_time", DateTime(timezone=True))
    download_to = Column("download_to", DateTime(timezone=True))
    created_at = Column("created_at", DateTime(timezone=True), default=func.now())