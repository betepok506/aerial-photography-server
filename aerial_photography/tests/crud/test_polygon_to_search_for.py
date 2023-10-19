import datetime
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate, PolygonsToSearchForUpdate,
    PolygonsToSearchForSearch
)
from aerial_photography.schemas.platform_name_sentinel import PlatformNameSentinelCreate
from aerial_photography.utils.geometry import convert_str_to_wkb, convert_polygon_to_str

# Координаты тестового полигона
COORD = [(44.680385, 54.721345),
         (46.226831, 54.781341),
         (46.306982, 53.698870),
         (44.392784, 53.779930)]

UPDATED_COORD = [(44.680385, 54.721345),
                 (36.226831, 54.781341),
                 (46.306982, 53.698870),
                 (44.392784, 56.779930)]


#
# @pytest.mark.asyncio
def test_create_polygons_to_search_for(db: Session) -> None:
    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    id_platform_name = 1
    id_polygon_type = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        id_platform_name=id_platform_name,
        id_polygon_type=id_polygon_type,
        footprint=str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {polygon.date}')
    # assert str(polygon.footprint) == str(convert_wkb(str_polygon))
    assert polygon.cloud_cover_percentage == cloud_cover_percentage
    assert polygon.id_platform_name == id_platform_name
    assert polygon.id_polygon_type == id_polygon_type
    # assert polygon.date == date


def test_get_polygons_to_search_for(db: Session) -> None:
    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    id_platform_name = 1
    id_polygon_type = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        id_platform_name=id_platform_name,
        id_polygon_type=id_polygon_type,
        footprint=str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    stored_polygon = crud.polygons_to_search_for.get(db=db, id=polygon.id)
    assert stored_polygon
    assert polygon.id_platform_name == stored_polygon.id_platform_name
    assert polygon.id_polygon_type == stored_polygon.id_polygon_type
    assert polygon.cloud_cover_percentage == stored_polygon.cloud_cover_percentage


def test_update_polygons_to_search_for(db: Session) -> None:
    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    id_platform_name = 1
    id_polygon_type = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        id_platform_name=id_platform_name,
        id_polygon_type=id_polygon_type,
        footprint=str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    updated_str_polygon = convert_polygon_to_str(COORD)
    updated_date = datetime.datetime.now()
    item_update = PolygonsToSearchForUpdate(
        id_platform_name=id_platform_name,
        id=polygon.id,
        footprint=updated_str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=updated_date,
        id_polygon_type=id_polygon_type
    )
    updated_polygon = crud.polygons_to_search_for.update(db=db, db_obj=polygon, obj_in=item_update)

    assert polygon.id == updated_polygon.id
    assert updated_polygon.id_polygon_type == id_polygon_type
    assert updated_polygon.cloud_cover_percentage == cloud_cover_percentage
    assert updated_polygon.id_platform_name == id_platform_name


def test_delete_polygons_to_search_for(db: Session) -> None:
    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    platform_name = 1
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        id_platform_name=platform_name,
        id_polygon_type=type_polygon,
        footprint=str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    removed_polygon = crud.polygons_to_search_for.remove(db=db, id=polygon.id)
    stored_polygon = crud.polygons_to_search_for.get(db=db, id=polygon.id)
    assert stored_polygon is None
    assert removed_polygon.id == polygon.id
    assert removed_polygon.id_platform_name == platform_name
    assert removed_polygon.id_polygon_type == type_polygon
    # assert removed_polygon.footprint == wkb_polygon
    assert removed_polygon.cloud_cover_percentage == cloud_cover_percentage
    # assert removed_polygon.date == date


def test_search_type_polygons_to_search_for(db: Session) -> None:
    '''
    На данный момент поиск осуществляется только по платформе
    '''
    platform_name = random_lower_string()
    platform_name_in = PlatformNameSentinelCreate(name=platform_name)
    platform = crud.platform_name_sentinel.create(db=db, obj_in=platform_name_in)

    str_polygon = convert_polygon_to_str(COORD)
    cloud_cover_percentage = [30, 60]
    id_polygon_type = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        id_platform_name=platform.id,
        id_polygon_type=id_polygon_type,
        footprint=str_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    search_polygon = crud.polygons_to_search_for.search(db=db, obj_in=PolygonsToSearchForSearch(
        platform_name=platform_name))
    assert len(search_polygon) == 1
    assert search_polygon[0].id == polygon.id
    assert search_polygon[0].id_platform_name == platform.id
    assert search_polygon[0].id_polygon_type == id_polygon_type
    # assert search_polygon.footprint == wkb_polygon
    assert search_polygon[0].cloud_cover_percentage == cloud_cover_percentage
    # assert search_polygon.date == date
