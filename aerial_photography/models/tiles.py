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


class Tiles(Base):
    __tablename__ = "tiles"

    id = Column('id', Integer, primary_key=True)
    # map_id = Column("map_id", Integer, ForeignKey("maps.id"))
    image = Column("image", LargeBinary)
    x = Column("x", Integer)
    y = Column("y", Integer)
    z = Column("z", Integer)
    created_at = Column("loading_time", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column("deleted", Boolean, default=False)
    # relationship_tiles2maps = relationship(
    #     "Maps",
    #     back_populates="relationship_maps2tiles"
    # )
