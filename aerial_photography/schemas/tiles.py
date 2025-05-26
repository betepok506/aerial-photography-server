from typing import Union, Iterable, List, Tuple, ByteString
from pydantic import BaseModel
from sqlalchemy import LargeBinary


class Tile(BaseModel):
    '''Схема модели в БД'''
    x: int
    y: int
    z: int
    image: bytes


class TilesCreate(Tile):
    pass


class TilesUpdate(Tile):
    pass


class TileSchema(BaseModel):
    '''Схема плитки'''
    x: int
    y: int
    z: int
    image: bytes


# class TileByCoordinate(BaseModel):
#     x: int
#     y: int
#     z: int


class TilesSchema(BaseModel):
    tiles: List[TileSchema]


class TilesCreateSchema(TilesSchema):
    pass


class TilesUpdateSchema(TilesSchema):
    pass


class TilesDeleteSchema(BaseModel):
    ids: List[int]

#
# class TilesUpdateUserGroupStatusSchema(BaseModel):
#     ids: List[int]
