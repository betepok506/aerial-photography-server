from sqlalchemy.orm import Session
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography import crud
from aerial_photography import schemas
from typing import Dict

DATA = {
    "id_platform_name": 0,
    "footprint": "POLYGON ((44.680385 54.721345, 46.226831 54.781341, 46.306982 53.69887, 44.392784 53.77993, 44.680385 54.721345))",
    "cloud_cover_percentage": [
        0, 30
    ],
    "date": "2023-10-25T07:24:27.748Z",
    "id_polygon_type": 0,
    "id_space_program": 0,
    "current_downloaded": 0,
    "need_to_download": 5
}

COORD = [(44.680385, 54.721345),
         (46.226831, 54.781341),
         (46.306982, 53.698870),
         (44.392784, 53.779930)]

UPDATED_COORD = [(44.680385, 54.721345),
                 (36.226831, 54.781341),
                 (46.306982, 53.698870),
                 (44.392784, 56.779930)]


def creating_dependent_records(db: Session):
    # Создаем платформу
    platform_name = random_lower_string()
    platform_name_in = schemas.PlatformNameCreate(name=platform_name)
    platform = crud.platform_name.create(db=db, obj_in=platform_name_in)

    # Создаем запись в базе для типа создаваемого полигона
    name = random_lower_string()
    polygon_in = schemas.TypePolygonsToSearchForCreate(name=name)
    type_polygon = crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)

    # Создаем запись о космической программе
    name = random_lower_string()
    space_program = crud.space_programs.create(db=db, obj_in=schemas.SpaceProgramsCreate(name=name))
    return platform, type_polygon, space_program


def update_template_data(original_data: Dict[str, str], updated_data: Dict[str, str]) -> Dict[str, str]:
    '''Функция для обновления шаблона новыми данными'''
    data = original_data.copy()
    for k, v in updated_data.items():
        data[k] = v
    return data
