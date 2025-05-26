from typing import Union, Iterable, List, Tuple
from datetime import datetime
from pydantic import BaseModel


class PolygonsToSearchFor(BaseModel):
    pass


class PolygonsToSearchForCreate(PolygonsToSearchFor):
    owner: int
    name: str
    footprint: str
    start_time: datetime
    end_time: datetime
    download_to: datetime

    # cloud_cover_percentage: List[int]
    # date: datetime
    # id_polygon_type: int
    # id_space_program: int
    # current_downloaded: int = 0
    # need_to_download: int

    # TODO: Добавить валидацию на длину cloud_cover_percentage == 2


class PolygonsToSearchForUpdate(PolygonsToSearchForCreate):
    id: int


# class PolygonsToSearchForSearch(BaseModel):
#     platform_name: str
#     skip: int = 0
#     limit: int = 100
#
#
# class PolygonsToSearchForSearchByPrograms(BaseModel):
#     name_space_program: str
#     skip: int = 0
#     limit: int = 100


class PolygonsToSearchForById(BaseModel):
    id: int
