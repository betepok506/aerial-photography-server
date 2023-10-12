from typing import Union, Iterable, List
from datetime import datetime
from pydantic import BaseModel


class TypePolygonsToSearchFor(BaseModel):
    name: str


class TypePolygonsToSearchForUpdate(TypePolygonsToSearchFor):
    id: int


class TypePolygonsToSearchForCreate(TypePolygonsToSearchFor):
    pass


class TypePolygonsToSearchForSearch(TypePolygonsToSearchFor):
    pass


class TypePolygonsToSearchForById(BaseModel):
    id: int
