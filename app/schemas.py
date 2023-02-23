from typing import Union, Iterable
from pydantic import BaseModel


class RequestPolygonsObject(BaseModel):
    lat_min: float
    lng_min: float
    lat_max: float
    lng_max: float
    cls_obj: Iterable[str]
