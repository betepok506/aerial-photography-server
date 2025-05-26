from typing import Union, Iterable, List
from datetime import datetime
from pydantic import BaseModel


class PlatformName(BaseModel):
    name: str


class PlatformNameUpdate(PlatformName):
    id: int


class PlatformNameCreate(PlatformName):
    pass


class PlatformNameSearch(PlatformName):
    pass


class PlatformNameSearchById(BaseModel):
    id: int
