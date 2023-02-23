import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Enum, Integer, MetaData, SmallInteger, String, Table, Boolean, Float
)
from geoalchemy2 import Geometry, Geography

Base = declarative_base()


# users_table = Table(
#     'users_tabdle',
#     Base.metadata,
#     Column('user_id', Integer, primary_key=True),
#     Column('email2', String(256), nullable=False, unique=True),
#     Column('name', String(collation='ru-RU-x-icu'), nullable=False),
#     Column('floor', SmallInteger, nullable=False),
#     Column('seat', SmallInteger, nullable=False),
#     Column('meat', SmallInteger, nullable=False),
# )
#
# poi_polygon = Table(
#     'poi_polygon',
#     Base.metadata,
#     Column('ogc_fid', Integer, primary_key=True),
#     Column('wkb_geometry', Geometry('POLYGON')),
#     Column('name', String(256)),
#     Column('name_en', String(256)),
#     Column('name_ru', String(256)),
#     Column('man_made', String(256)),
#     Column('leisure', String(256)),
#     Column('amenity', String(256)),
#     Column('office', String(80)),
#     Column('shop', String(80)),
#     Column('tourism', String(80)),
#     Column('sport', String(80)),
#     Column('osm_type', String(80)),
#     Column('osm_id', Integer),
# )


class PoiPolygon(Base):
    __tablename__ = "poi_polygon"

    ogc_fid = Column('ogc_fid', Integer, primary_key=True)
    # wkb_geometry = Column('wkb_geometry', Geometry('POLYGON', srid=4326))
    wkb_geometry = Column('wkb_geometry', Geometry('POLYGON'))
    name = Column('name', String(256))
    name_en = Column('name_en', String(256))
    name_ru = Column('name_ru', String(256))
    man_made = Column('man_made', String(256))
    leisure = Column('leisure', String(256))
    amenity = Column('amenity', String(256))
    office = Column('office', String(80))
    shop = Column('shop', String(80))
    tourism = Column('tourism', String(80))
    sport = Column('sport', String(80))
    osm_type = Column('osm_type', String(80))
    osm_id = Column('osm_id', Integer)


class ClassObjectDisplay(Base):
    __tablename__ = "class_object_display"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(80), nullable=None)
    value = Column('value', Integer, unique=True, nullable=None)
    color = Column('color', String(40))
    max_display_zoom = Column('max_display_zoom', Integer)
    min_display_zoom = Column('min_display_zoom', Integer)
    line_width = Column('line_width', Integer)
    polygon_transparency = Column('polygon_transparency', Float)
    clickability = Column('clickability', Boolean, default=True)
