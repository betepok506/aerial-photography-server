from aerial_photography.database.base_class import Base
from sqlalchemy import (
    Column,
    ARRAY,
    Integer,
    DateTime,
    String,
    ForeignKey
)


class TypePolygonsToSearchFor(Base):
    __tablename__ = "type_polygons_to_search_for"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(60))
