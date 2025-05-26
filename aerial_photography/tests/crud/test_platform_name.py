# from sqlalchemy.ext.asyncio import AsyncSession
# import pytest_asyncio
import pytest
from sqlalchemy.orm import Session
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.platform_name import PlatformNameCreate, PlatformNameUpdate


def test_create_platform_name(db: Session) -> None:
    platform_name = random_lower_string()
    platform_name_in = PlatformNameCreate(name=platform_name)
    platform = crud.platform_name.create(db=db, obj_in=platform_name_in)
    assert platform.name == platform_name


def test_get_platform_name(db: Session) -> None:
    platform_name = random_lower_string()
    platform_name_in = PlatformNameCreate(name=platform_name)
    platform = crud.platform_name.create(db=db, obj_in=platform_name_in)
    stored_platform = crud.platform_name.get(db=db, id=platform.id)
    assert stored_platform
    assert platform.id == stored_platform.id
    assert platform.name == stored_platform.name


def test_update_platform_name(db: Session) -> None:
    platform_name = random_lower_string()
    platform_name_in = PlatformNameCreate(name=platform_name)
    platform = crud.platform_name.create(db=db, obj_in=platform_name_in)

    new_platform = random_lower_string()
    item_update = PlatformNameUpdate(id=platform.id, name=new_platform)
    updated_platform = crud.platform_name.update(db=db, db_obj=platform, obj_in=item_update)
    assert platform.id == updated_platform.id
    assert updated_platform.name == new_platform


def test_delete_platform_name(db: Session) -> None:
    platform_name = random_lower_string()
    platform_name_in = PlatformNameCreate(name=platform_name)
    platform = crud.platform_name.create(db=db, obj_in=platform_name_in)

    removed_platform = crud.platform_name.remove(db=db, id=platform.id)
    stored_platform = crud.platform_name.get(db=db, id=platform.id)
    assert stored_platform is None
    assert removed_platform.id == platform.id
    assert removed_platform.name == platform_name
