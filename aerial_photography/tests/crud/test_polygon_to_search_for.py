import datetime

from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate, PolygonsToSearchForUpdate,
    PolygonsToSearchForSearch
)
from aerial_photography.schemas.platform_name_sentinel import PlatformNameSentinelCreate
from aerial_photography.utils.geometry import convert_wkb

# Координаты тестового полигона
COORD = [(44.680385, 54.721345),
         (46.226831, 54.781341),
         (46.306982, 53.698870),
         (44.392784, 53.779930)]

UPDATED_COORD = [(44.680385, 54.721345),
                 (36.226831, 54.781341),
                 (46.306982, 53.698870),
                 (44.392784, 56.779930)]


@pytest.mark.asyncio
async def test_create_polygons_to_search_for(db: AsyncSession) -> None:
    wkb_polygon = convert_wkb(COORD)
    cloud_cover_percentage = [30, 60]
    platform_name = 1
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        platform_name=platform_name,
        type_polygon=type_polygon,
        footprint=wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = await crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    assert polygon.polygon_wkb == wkb_polygon
    assert polygon.cloud_cover_percentage == cloud_cover_percentage
    assert polygon.platform_name == platform_name
    assert polygon.type_polygon == type_polygon
    assert polygon.date == date


@pytest.mark.asyncio
async def test_get_polygons_to_search_for(db: AsyncSession) -> None:
    wkb_polygon = convert_wkb(COORD)
    cloud_cover_percentage = [30, 60]
    platform_name = 1
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        platform_name=platform_name,
        type_polygon=type_polygon,
        footprint=wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = await crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    stored_polygon = await crud.polygons_to_search_for.get(db=db, id=polygon.id)
    assert stored_polygon
    assert polygon.id == stored_polygon.id
    assert polygon.name == stored_polygon.name

    # TODO: Дописать тестирование PolygonsToSearchFor, разобраться точно ли оно тестируется


@pytest.mark.asyncio
async def test_update_polygons_to_search_for(db: AsyncSession) -> None:
    wkb_polygon = convert_wkb(COORD)
    cloud_cover_percentage = [30, 60]
    platform_name = 1
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        platform_name=platform_name,
        type_polygon=type_polygon,
        footprint=wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = await crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    updated_wkb_polygon = convert_wkb(COORD)
    updated_date = datetime.datetime.now()
    item_update = PolygonsToSearchForCreate(
        platform_name=platform_name,
        type_polygon=type_polygon,
        footprint=updated_wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=updated_date
    )
    updated_polygon = await crud.polygons_to_search_for.update(db=db, db_obj=polygon, obj_in=item_update)

    assert polygon.id == updated_polygon.id
    assert updated_polygon.footprint == updated_wkb_polygon
    assert updated_polygon.date == updated_date


@pytest.mark.asyncio
async def test_delete_polygons_to_search_for(db: AsyncSession) -> None:
    wkb_polygon = convert_wkb(COORD)
    cloud_cover_percentage = [30, 60]
    platform_name = 1
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        platform_name=platform_name,
        type_polygon=type_polygon,
        footprint=wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = await crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    removed_polygon = await crud.type_polygons_to_search_for.remove(db=db, id=polygon.id)
    stored_polygon = await crud.type_polygons_to_search_for.get(db=db, id=polygon.id)
    assert stored_polygon is None
    assert removed_polygon.id == polygon.id
    assert removed_polygon.platform_name == platform_name
    assert removed_polygon.type_polygon == type_polygon
    assert removed_polygon.footprint == wkb_polygon
    assert removed_polygon.cloud_cover_percentage == cloud_cover_percentage
    assert removed_polygon.date == date


@pytest.mark.asyncio
async def test_search_type_polygons_to_search_for(db: AsyncSession) -> None:
    '''
    На данный момент поиск осуществляется только по платформе
    '''
    platform_name = random_lower_string()
    platform_name_in = PlatformNameSentinelCreate(name=platform_name)
    platform = await crud.platform_name_sentinel.create(db=db, obj_in=platform_name_in)

    wkb_polygon = convert_wkb(COORD)
    cloud_cover_percentage = [30, 60]
    type_polygon = 1
    date = datetime.datetime.now()

    polygon_in = PolygonsToSearchForCreate(
        platform_name=platform.id,
        type_polygon=type_polygon,
        footprint=wkb_polygon,
        cloud_cover_percentage=cloud_cover_percentage,
        date=date
    )
    polygon = await crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)

    search_polygon = await crud.type_polygons_to_search_for.search(db=db, obj_in=PolygonsToSearchForSearch(
        platform_name=platform_name))
    assert search_polygon.id == polygon.id
    assert search_polygon.platform_name != platform.id
    assert search_polygon.type_polygon == type_polygon
    assert search_polygon.footprint == wkb_polygon
    assert search_polygon.cloud_cover_percentage == cloud_cover_percentage
    assert search_polygon.date == date
    assert 1 == 2
