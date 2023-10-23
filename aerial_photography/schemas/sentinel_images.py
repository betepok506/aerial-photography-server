from typing import Union, Iterable, List, Tuple
from datetime import datetime
from pydantic import BaseModel


class SentinelImages(BaseModel):
    id_platform_name: int
    filename: str
    footprint: str
    identifier: str
    begin_position: datetime
    end_position: datetime


class SentinelImagesCreate(SentinelImages):
    pass


class SentinelImagesUpdate(SentinelImagesCreate):
    id: int


class SentinelImagesSearch(BaseModel):
    platform_name: str


class SentinelImagesSearchById(BaseModel):
    id: int
