from typing import Union, Iterable
from pydantic import BaseModel


class RequestPolygonsObject(BaseModel):
    lat_min: float
    lng_min: float
    lat_max: float
    lng_max: float
    cls_obj: Iterable[str]


class Tile(BaseModel):
    map_id: int
    x: int
    y: int
    z: int


class Tiles_schemas(BaseModel):
    tiles: Iterable[Tile]


class MapInfo(BaseModel):
    map_name: str
    hash_md5: str
