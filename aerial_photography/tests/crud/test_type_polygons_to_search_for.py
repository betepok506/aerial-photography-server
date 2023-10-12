from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.type_polygons_to_search_for import (
    TypePolygonsToSearchForCreate, TypePolygonsToSearchForUpdate,
    TypePolygonsToSearchForSearch
)


@pytest.mark.asyncio
async def test_create_type_polygons_to_search_for(db: AsyncSession) -> None:
    name = random_lower_string()
    polygon_in = TypePolygonsToSearchForCreate(name=name)
    polygon = await crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)
    assert polygon.name == name


@pytest.mark.asyncio
async def test_get_type_polygons_to_search_for(db: AsyncSession) -> None:
    name = random_lower_string()
    polygon_in = TypePolygonsToSearchForCreate(name=name)
    polygon = await crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)
    stored_polygon = await crud.platform_name_sentinel.get(db=db, id=polygon.id)
    assert stored_polygon
    assert polygon.id == stored_polygon.id
    assert polygon.name == stored_polygon.name


@pytest.mark.asyncio
async def test_update_type_polygons_to_search_for(db: AsyncSession) -> None:
    name = random_lower_string()
    polygon_in = TypePolygonsToSearchForCreate(name=name)
    polygon = await crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)

    new_polygon = random_lower_string()
    item_update = TypePolygonsToSearchForUpdate(name=new_polygon)
    updated_polygon = await crud.type_polygons_to_search_for.update(db=db, db_obj=polygon, obj_in=item_update)
    assert polygon.id == updated_polygon.id
    assert updated_polygon.name == new_polygon


@pytest.mark.asyncio
async def test_delete_type_polygons_to_search_for(db: AsyncSession) -> None:
    name = random_lower_string()
    polygon_in = TypePolygonsToSearchForCreate(name=name)
    polygon = await crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)

    removed_polygon = await crud.type_polygons_to_search_for.remove(db=db, id=polygon.id)
    stored_polygon = await crud.type_polygons_to_search_for.get(db=db, id=polygon.id)
    assert stored_polygon is None
    assert removed_polygon.id == polygon.id
    assert removed_polygon.name == name


@pytest.mark.asyncio
async def test_search_type_polygons_to_search_for(db: AsyncSession) -> None:
    name = random_lower_string()
    polygon_in = TypePolygonsToSearchForCreate(name=name)
    polygon = await crud.type_polygons_to_search_for.create(db=db, obj_in=polygon_in)

    search_polygon = await crud.type_polygons_to_search_for.search(db=db, obj_in=TypePolygonsToSearchForSearch(
        name=name))
    assert search_polygon.id == polygon.id
    assert search_polygon.name == name
