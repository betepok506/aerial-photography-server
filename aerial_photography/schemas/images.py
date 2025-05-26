from typing import Union, Iterable, List, Tuple
from datetime import datetime
from pydantic import BaseModel


class Images(BaseModel):
    id_platform_name: int
    filename: str
    footprint: str
    identifier: str
    begin_position: datetime
    end_position: datetime


class ImagesCreate(Images):
    pass


class ImagesUpdate(ImagesCreate):
    id: int


class ImagesSearch(BaseModel):
    platform_name: str


class ImagesSearchById(BaseModel):
    id: int
