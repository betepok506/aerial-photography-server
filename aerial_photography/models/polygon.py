from aerial_photography.database.base_class import Base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    ARRAY,
    Integer,
    DateTime,
    ForeignKey
)


class PolygonsToSearchFor(Base):
    __tablename__ = "polygons_to_search_for"

    id = Column('id', Integer, primary_key=True)
    platform_name = Column('platform_name', Integer, ForeignKey("platform_name_sentinel.id"))
    collection = Column('collection', Integer, ForeignKey("collection_sentinel.id"))

    footprint = Column('footprint', Geometry('POLYGON'))
    cloud_cover_percentage = Column("cloud_cover_percentage", ARRAY(Integer))
    date = Column("date", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
