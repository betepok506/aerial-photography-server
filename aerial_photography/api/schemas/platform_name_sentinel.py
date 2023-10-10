from typing import Union, Iterable, List
from datetime import datetime
from pydantic import BaseModel


class PlatformNameSentinel(BaseModel):
    name: str


class PlatformNameSentinelUpdate(PlatformNameSentinel):
    id: int


class PlatformNameSentinelCreate(PlatformNameSentinel):
    pass


class PlatformNameSentinelSearch(PlatformNameSentinel):
    pass


class PlatformNameSentinelSearchById(BaseModel):
    id: int
