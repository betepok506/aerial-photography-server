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
    id_platform_name = Column('id_platform_name', Integer, ForeignKey("platform_name_sentinel.id"))
    id_polygon_type = Column('id_polygon_type', Integer, ForeignKey("type_polygons_to_search_for.id"))
    # collection = Column('collection', Integer, ForeignKey("collection_sentinel.id"))

    footprint = Column('footprint', Geometry('POLYGON'))
    cloud_cover_percentage = Column("cloud_cover_percentage", ARRAY(Integer))
    date = Column("date", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

