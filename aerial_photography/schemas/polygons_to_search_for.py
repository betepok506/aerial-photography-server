from typing import Union, Iterable, List, Tuple
from datetime import datetime
from pydantic import BaseModel


class PolygonsToSearchFor(BaseModel):
    platform_name: int


class PolygonsToSearchForUpdate(PolygonsToSearchFor):
    id: int
    footprint: str
    cloud_cover_percentage: List[Tuple[int, int]]
    date: datetime
    type_polygon: int


class PolygonsToSearchForCreate(PolygonsToSearchFor):
    footprint: str
    cloud_cover_percentage: List[Tuple[int, int]]
    date: datetime
    type_polygon: int


class PolygonsToSearchForSearch(PolygonsToSearchFor):
    pass


class PolygonsToSearchForById(BaseModel):
    id: int
