import datetime
from sqlalchemy.orm import Session
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.sentinel_images import (
    SentinelImagesCreate, SentinelImagesUpdate,
    SentinelImagesSearch
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


def test_create_sentinel_images(db: Session) -> None:
    filename = random_lower_string(80)
    identifier = random_lower_string(90)
    str_polygon = convert_polygon_to_str(COORD)
    platform_id = 1
    begin_position = datetime.datetime.now()
    end_position = datetime.datetime.now()

    images_in = SentinelImagesCreate(
        platform_id=platform_id,
        filename=filename,
        footprint=str_polygon,
        identifier=identifier,
        begin_position=begin_position,
        end_position=end_position,
    )
    image = crud.sentinel_images.create(db=db, obj_in=images_in)

    assert image.platform_id == platform_id
    assert image.identifier == identifier
    assert image.filename == filename
    # assert image.begin_position == begin_position
    # assert image.begin_position == begin_position
    # assert image.end_position == end_position


def test_get_sentinel_images(db: Session) -> None:
    filename = random_lower_string(80)
    identifier = random_lower_string(90)
    str_polygon = convert_polygon_to_str(COORD)
    platform_id = 1
    begin_position = datetime.datetime.now()
    end_position = datetime.datetime.now()

    images_in = SentinelImagesCreate(
        platform_id=platform_id,
        filename=filename,
        footprint=str_polygon,
        identifier=identifier,
        begin_position=begin_position,
        end_position=end_position,
    )
    image = crud.sentinel_images.create(db=db, obj_in=images_in)

    stored_image = crud.sentinel_images.get(db=db, id=image.id)
    assert stored_image
    assert image.platform_id == stored_image.platform_id
    assert image.filename == stored_image.filename
    assert image.identifier == stored_image.identifier
    # assert image.begin_position == stored_image.begin_position
    # assert image.end_position == stored_image.end_position


def test_update_sentinel_images(db: Session) -> None:
    filename = random_lower_string(80)
    identifier = random_lower_string(90)
    str_polygon = convert_polygon_to_str(COORD)
    platform_id = 1
    begin_position = datetime.datetime.now()
    end_position = datetime.datetime.now()

    image_in = SentinelImagesCreate(
        platform_id=platform_id,
        filename=filename,
        footprint=str_polygon,
        identifier=identifier,
        begin_position=begin_position,
        end_position=end_position,
    )
    image = crud.sentinel_images.create(db=db, obj_in=image_in)

    updated_str_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_date = datetime.datetime.now()
    updated_identifier = random_lower_string(90)
    image_update = SentinelImagesCreate(
        platform_id=platform_id,
        filename=filename,
        footprint=updated_str_polygon,
        identifier=updated_identifier,
        begin_position=begin_position,
        end_position=updated_date,
    )
    updated_image = crud.sentinel_images.update(db=db, db_obj=image, obj_in=image_update)

    assert image.id == updated_image.id
    assert updated_image.identifier == updated_identifier
    assert updated_image.filename == filename
    assert updated_image.platform_id == platform_id
    # assert updated_image.begin_position == begin_position
    # assert updated_image.end_position == updated_date


def test_delete_sentinel_images(db: Session) -> None:
    filename = random_lower_string(80)
    identifier = random_lower_string(90)
    str_polygon = convert_polygon_to_str(COORD)
    platform_id = 1
    begin_position = datetime.datetime.now()
    end_position = datetime.datetime.now()

    image_in = SentinelImagesCreate(
        platform_id=platform_id,
        filename=filename,
        footprint=str_polygon,
        identifier=identifier,
        begin_position=begin_position,
        end_position=end_position,
    )
    image = crud.sentinel_images.create(db=db, obj_in=image_in)

    removed_image = crud.sentinel_images.remove(db=db, id=image.id)
    stored_image = crud.sentinel_images.get(db=db, id=image.id)
    assert stored_image is None
    assert removed_image.id == image.id
    assert removed_image.platform_id == platform_id
    assert removed_image.filename == filename
    assert removed_image.identifier == identifier
    # assert removed_image.begin_position == begin_position
    # assert removed_image.end_position == end_position


# @pytest.mark.asyncio
def test_search_type_polygons_to_search_for(db: Session) -> None:
    '''
    На данный момент поиск осуществляется только по платформе
    '''

    platform_name = random_lower_string()
    platform_name_in = PlatformNameSentinelCreate(name=platform_name)
    platform = crud.platform_name_sentinel.create(db=db, obj_in=platform_name_in)

    filename = random_lower_string(80)
    identifier = random_lower_string(90)
    str_polygon = convert_polygon_to_str(COORD)
    begin_position = datetime.datetime.now()
    end_position = datetime.datetime.now()

    image_in = SentinelImagesCreate(
        platform_id=platform.id,
        filename=filename,
        footprint=str_polygon,
        identifier=identifier,
        begin_position=begin_position,
        end_position=end_position,
    )
    image = crud.sentinel_images.create(db=db, obj_in=image_in)

    search_image = crud.sentinel_images.search(db=db, obj_in=SentinelImagesSearch(
        platform_name=platform_name))

    assert len(search_image) == 1
    assert search_image[0].id == image.id
    assert search_image[0].platform_id == platform.id
    assert search_image[0].filename == filename
    assert search_image[0].identifier == identifier
    # assert search_image[0].begin_position == begin_position
    # assert search_image[0].end_position == end_position
