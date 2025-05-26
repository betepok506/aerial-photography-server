from aerial_photography.database.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class PlatformName(Base):
    '''
    Таблица содержит название платформы космических спутников
    '''
    __tablename__ = "platform_name"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(60))
