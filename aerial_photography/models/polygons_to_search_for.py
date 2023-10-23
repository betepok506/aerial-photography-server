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

    # TODO: Добавить космические программы в полигоны
    # TODO: Platfrom name сделать универсальными в зависимости от программы, добавить кол-во загрузок или диапазон времени
    # Сделать запрос полигонов в зависимости от переданных параметров: https://stackoverflow.com/questions/31063860/conditionally-filtering-in-sqlalchemy
    # Написать тесты на api polygons_to_search_for
    # Пофиксить тесты crud polygons_to_search_for

    id = Column('id', Integer, primary_key=True)
    id_platform_name = Column('id_platform_name', Integer, ForeignKey("platform_name.id")) # Идентификатор платформы
    id_polygon_type = Column('id_polygon_type', Integer, ForeignKey("type_polygons_to_search_for.id")) # Идентификатор типа полигона
    id_space_program = Column('id_space_program', Integer, ForeignKey("space_programs.id")) # Идентификатор космической программы
    # collection = Column('collection', Integer, ForeignKey("collection_sentinel.id"))
    current_downloaded = Column('current_downloaded', Integer) # Сколько раз уже скачанно
    need_to_download = Column('need_to_download', Integer) # Сколько раз необходимо скачать

    footprint = Column('footprint', Geometry('POLYGON')) # Координаты полигона, в котором будут запрашиваться снимки
    cloud_cover_percentage = Column("cloud_cover_percentage", ARRAY(Integer)) # Добустимый диапазон облачности
    date = Column("date", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) # Время добавления полигона
