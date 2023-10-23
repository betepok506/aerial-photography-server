from typing import Union, Iterable, List, Tuple
from datetime import datetime
from pydantic import BaseModel


class PolygonsToSearchFor(BaseModel):
    id_platform_name: int


class PolygonsToSearchForCreate(PolygonsToSearchFor):
    footprint: str
    cloud_cover_percentage: List[int]
    date: datetime
    id_polygon_type: int
    # TODO: Добавить валидацию на длину cloud_cover_percentage == 2


class PolygonsToSearchForUpdate(PolygonsToSearchForCreate):
    id: int


class PolygonsToSearchForSearch(BaseModel):
    platform_name: str


class PolygonsToSearchForById(BaseModel):
    id: int

