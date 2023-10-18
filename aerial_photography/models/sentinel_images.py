from aerial_photography.database.base_class import Base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    ARRAY,
    Integer,
    DateTime,
    String,
    ForeignKey
)


class SentinelImages(Base):
    __tablename__ = "sentinel_images"

    id = Column('id', Integer, primary_key=True)
    filename = Column('filename', String(120))
    footprint = Column('footprint', Geometry('POLYGON'))
    platform_id = Column('platform_id', Integer, ForeignKey("platform_name_sentinel.id"))
    # product_type
    identifier = Column('identifier', String(120))
    begin_position = Column("begin_position", DateTime(timezone=True), server_default=func.now())
    end_position = Column("end_position", DateTime(timezone=True), server_default=func.now())
