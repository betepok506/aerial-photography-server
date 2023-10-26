from aerial_photography.utils.geometry import convert_str_to_wkb, convert_polygon_to_str
from aerial_photography import crud
from aerial_photography.database.session import SessionLocal
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate, PolygonsToSearchForUpdate,
    PolygonsToSearchForSearch
)
from aerial_photography import schemas
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.platform_name import PlatformNameCreate
import datetime
from fastapi.testclient import TestClient
from aerial_photography.config import settings
from aerial_photography.app import app
from typing import Dict, Generator


COORD = [(44.680385, 54.721345),
         (46.226831, 54.781341),
         (46.306982, 53.698870),
         (44.392784, 53.779930)]



if __name__ == "__main__":
    db = SessionLocal()
    # Создаем платформу
    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    id_platform_name = 1
    id_polygon_type = 1
    need_to_download = 5
    id_space_program = 1
    current_downloaded = 0
    date = datetime.datetime.now()
    #
    # polygon_in = PolygonsToSearchForCreate(
    #     id_platform_name=id_platform_name,
    #     id_polygon_type=id_polygon_type,
    #     id_space_program=id_space_program,
    #     current_downloaded=current_downloaded,
    #     need_to_download=need_to_download,
    #     footprint=str_polygon,
    #     cloud_cover_percentage=cloud_cover_percentage,
    #     date=date
    # )
    # polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    stored_polygon = crud.polygons_to_search_for.get(db=db, id=2)
    print(8)