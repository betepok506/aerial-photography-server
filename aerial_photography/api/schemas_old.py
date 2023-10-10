from typing import Union, Iterable, List
from datetime import datetime
from pydantic import BaseModel


# class PolygonToUpload(BaseModel):
#     '''
#     Схема для добавления информации о полигонов в базу для последующего запроса снимков внитру этих полигонов
#     '''
#     polygon: str
#     platform_name: int or str
#     collection: int or str
#     date_from: datetime or None
#     date_to: datetime or None
#     type_polygon: int


class RequestPolygonsObject(BaseModel):
    lat_min: float
    lng_min: float
    lat_max: float
    lng_max: float
    cls_obj: Iterable[str]


class Tile(BaseModel):
    map_name: str
    x: int
    y: int
    z: int
    image: bytes


class TilesSchemas(BaseModel):
    tiles: List[Tile]


class RequestsRawTiles(BaseModel):
    map_name: str
    network_name: str
    cnt: int


class MapInfo(BaseModel):
    map_name: str
    # hash_md5: str
