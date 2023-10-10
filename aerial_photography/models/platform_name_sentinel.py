from aerial_photography.database.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class PlatformNameSentinel(Base):
    __tablename__ = "platform_name_sentinel"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(60))
