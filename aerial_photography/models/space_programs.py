from aerial_photography.database.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class SpacePrograms(Base):
    __tablename__ = "space_programs"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(60))
