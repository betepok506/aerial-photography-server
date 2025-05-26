import datetime

from fastapi.testclient import TestClient
from aerial_photography.config import settings
from sqlalchemy.orm import Session
from aerial_photography.tests.api.v1.polygons_to_search_for.utils import creating_dependent_records, \
    update_template_data, DATA, COORD
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.utils.geometry import convert_polygon_to_str
from aerial_photography.utils.utils import convert_datetime_to_str


def test_get_image(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API получения снимка
    '''
    filename = random_lower_string(70)
    identifier = random_lower_string(70)
    begin_position = convert_datetime_to_str(datetime.datetime.now())
    end_position = convert_datetime_to_str(datetime.datetime.now())

    platform, type_polygon, space_program = creating_dependent_records(db)
    data = {
        'filename': filename,
        'footprint': convert_polygon_to_str(COORD),
        'id_platform_name': platform.id,
        'identifier': identifier,
        'begin_position': begin_position,
        'end_position': end_position
    }
    response = client.post(
        f"{settings.API_V1_STR}/image/create_image", json=data,
    )

    assert response.status_code == 200

    content = response.json()
    requested_id = content['id']
    response = client.get(
        f"{settings.API_V1_STR}/image/get_image", params={'id': requested_id},
    )

    assert response.status_code == 200
    content = response.json()

    assert content["id_platform_name"] == data["id_platform_name"]
    assert content["filename"] == data["filename"]
    assert content["identifier"] == data["identifier"]
    assert content["footprint"] == data["footprint"]


def test_get_image_error_not_found(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API получения отсутствующего снимка
    '''

    response = client.get(
        f"{settings.API_V1_STR}/image/get_image", params={'id': 0},
    )

    assert response.status_code == 404
