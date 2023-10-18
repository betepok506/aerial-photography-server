# import sqlalchemy
# from sqlalchemy.sql import func
# from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy.ext.declarative import declarative_base
# from aerial_photography.database.base_class import Base
# from sqlalchemy import (
#     Column,
#     ARRAY,
#     Enum,
#     Integer,
#     LargeBinary,
#     MetaData,
#     SmallInteger,
#     String,
#     Table,
#     Boolean,
#     Float,
#     DateTime,
#     ForeignKey
# )
# from geoalchemy2 import Geometry, Geography
# from sqlalchemy.orm import DeclarativeBase
#
#
# # TODO: Разобраться с вызовов after_create 2 раза
# # Base = declarative_base()
#
# # class Base(DeclarativeBase):
# #     pass
#
#
# # users_table = Table(
# #     'users_tabdle',
# #     Base.metadata,
# #     Column('user_id', Integer, primary_key=True),
# #     Column('email2', String(256), nullable=False, unique=True),
# #     Column('name', String(collation='ru-RU-x-icu'), nullable=False),
# #     Column('floor', SmallInteger, nullable=False),
# #     Column('seat', SmallInteger, nullable=False),
# #     Column('meat', SmallInteger, nullable=False),
# # )
# #
# # poi_polygon = Table(
# #     'poi_polygon',
# #     Base.metadata,
# #     Column('ogc_fid', Integer, primary_key=True),
# #     Column('wkb_geometry', Geometry('POLYGON')),
# #     Column('name', String(256)),
# #     Column('name_en', String(256)),
# #     Column('name_ru', String(256)),
# #     Column('man_made', String(256)),
# #     Column('leisure', String(256)),
# #     Column('amenity', String(256)),
# #     Column('office', String(80)),
# #     Column('shop', String(80)),
# #     Column('tourism', String(80)),
# #     Column('sport', String(80)),
# #     Column('osm_type', String(80)),
# #     Column('osm_id', Integer),
# # )
#
#
# class PoiPolygon(Base):
#     __tablename__ = "poi_polygon"
#
#     ogc_fid = Column('ogc_fid', Integer, primary_key=True)
#     # wkb_geometry = Column('wkb_geometry', Geometry('POLYGON', srid=4326))
#     wkb_geometry = Column('wkb_geometry', Geometry('POLYGON'))
#     name = Column('name', String(256))
#     name_en = Column('name_en', String(256))
#     name_ru = Column('name_ru', String(256))
#     man_made = Column('man_made', String(256))
#     leisure = Column('leisure', String(256))
#     amenity = Column('amenity', String(256))
#     office = Column('office', String(80))
#     shop = Column('shop', String(80))
#     tourism = Column('tourism', String(80))
#     sport = Column('sport', String(80))
#     osm_type = Column('osm_type', String(80))
#     osm_id = Column('osm_id', Integer)
#
#
# class ClassObjectDisplay(Base):
#     __tablename__ = "class_object_display"
#
#     id = Column('id', Integer, primary_key=True)
#     name = Column('name', String(80), nullable=None)
#     value = Column('value', Integer, unique=True, nullable=None)
#     color = Column('color', String(40))
#     max_display_zoom = Column('max_display_zoom', Integer)
#     min_display_zoom = Column('min_display_zoom', Integer)
#     line_width = Column('line_width', Integer)
#     polygon_transparency = Column('polygon_transparency', Float)
#     clickability = Column('clickability', Boolean, default=True)
#
#
# class Maps(Base):
#     __tablename__ = "maps"
#
#     id = Column('id', Integer, primary_key=True)
#     name = Column('name', String(80), nullable=None)
#     # md5 = Column('md5', String(34), nullable=None)
#     relationship_maps2tiles = relationship(
#         "Tiles",
#         back_populates="relationship_tiles2maps"
#     )
#
#
# class Tiles(Base):
#     __tablename__ = "tiles"
#
#     id = Column('id', Integer, primary_key=True)
#     map_id = Column("map_id", Integer, ForeignKey("maps.id"))
#     image = Column("image", LargeBinary)
#     x = Column("x", Integer)
#     y = Column("y", Integer)
#     z = Column("z", Integer)
#     loading_time = Column("loading_time", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
#     deleted = Column("deleted", Boolean, default=False)
#     # relationship_tiles2detected_objects = relationship(
#     #     "DetectedObjects",
#     #     back_populates="relationship_detected_objects2tiles"
#     # )
#     relationship_tiles2maps = relationship(
#         "Maps",
#         back_populates="relationship_maps2tiles"
#     )
#
#
# class NeuralNetwork(Base):
#     __tablename__ = "neural_network"
#
#     id = Column('id', Integer, primary_key=True)
#     name_neural_network = Column("name_neural_network", String(80))
#     relationship_neural_network2detected_objects = relationship(
#         "DetectedObjects",
#         back_populates="relationship_detected_objects2neural_network"
#     )
#
#
# class DetectedObjects(Base):
#     __tablename__ = "detected_objects"
#
#     id = Column('id', Integer, primary_key=True)
#     tile_id = Column("tile_id", Integer, ForeignKey("tiles.id"))
#     neural_network_id = Column("neural_network_id", Integer, ForeignKey("neural_network.id"))
#     wkb_geometry = Column('wkb_geometry', Geometry('POLYGON'))
#     attributes_id = Column("attributes_id", Integer)
#     # relationship_detected_objects2tiles = relationship(
#     #     "Tiles",
#     #     back_populates="relationship_tiles2detected_objects"
#     # )
#     relationship_detected_objects2neural_network = relationship(
#         "NeuralNetwork",
#         back_populates="relationship_neural_network2detected_objects"
#     )
#
#
# class PolygonsToSearchFor(Base):
#     __tablename__ = "polygons_to_search_for"
#
#     id = Column('id', Integer, primary_key=True)
#     platform_name = Column('platform_name', Integer, ForeignKey("platform_name_sentinel.id"))
#     collection = Column('collection', Integer, ForeignKey("collection_sentinel.id"))
#
#     footprint = Column('footprint', Geometry('POLYGON'))
#     cloud_cover_percentage = Column("cloud_cover_percentage", ARRAY(Integer))
#     date = Column("date", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
#
#
# class CollectionSentinel(Base):
#     __tablename__ = "collection_sentinel"
#
#     id = Column('id', Integer, primary_key=True)
#     name = Column('name', String(60))
#
#
# # class PlatformNameSentinel(Base):
# #     __tablename__ = "platform_name_sentinel"
# #
# #     id = Column('id', Integer, primary_key=True)
# #     name = Column('name', String(60))
