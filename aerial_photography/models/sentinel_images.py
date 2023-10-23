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


class Images(Base):
    '''
    Данная таблица содержит информацию о загруженных снимках ДЗЗ
    '''
    __tablename__ = "images"

    id = Column('id', Integer, primary_key=True)
    filename = Column('filename', String(120)) # Имя файла, содержащего изображение
    footprint = Column('footprint', Geometry('POLYGON')) # Полигон, отвечающий за площадь снимка
    id_platform_name = Column('id_platform_name', Integer, ForeignKey("platform_name.id")) # Идентификатор имени платформы снимка
    # product_type
    identifier = Column('identifier', String(120)) # Уникальный идентификатор снимка
    begin_position = Column("begin_position", DateTime(timezone=True), server_default=func.now()) # Время начала получения снимка
    end_position = Column("end_position", DateTime(timezone=True), server_default=func.now()) # Время окончания получения снимка
