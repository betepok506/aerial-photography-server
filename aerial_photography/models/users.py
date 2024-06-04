from aerial_photography.database.base_class import Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    username = Column("username", String)
    login = Column("login", String)
    password = Column("password", String)
    polygons_to_search_for_relationship = relationship("PolygonsToSearchFor", back_populates="owner_relationship")

    created_at = Column("loading_time", DateTime(timezone=True), server_default=func.now())