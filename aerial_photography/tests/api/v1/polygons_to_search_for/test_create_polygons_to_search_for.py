from fastapi.testclient import TestClient
from aerial_photography.config import settings
from sqlalchemy.orm import Session
from aerial_photography.tests.api.v1.polygons_to_search_for.utils import creating_dependent_records, \
    update_template_data, DATA


def test_create_polygon_to_search_for(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API создания полигона
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
    }
    data = update_template_data(DATA, updated_data)

    response = client.post(
        f"{settings.API_V1_STR}/polygon/create_polygon_to_search_for", json=data,
    )

    assert response.status_code == 200

    content = response.json()
    assert content["id_platform_name"] == data["id_platform_name"]
    assert content["id_polygon_type"] == data["id_polygon_type"]
    assert content["id_space_program"] == data["id_space_program"]
    assert content["footprint"] == data["footprint"]
    assert content["current_downloaded"] == data["current_downloaded"]
    assert content["need_to_download"] == data["need_to_download"]
    # assert content["date"] == data["date"]


def test_create_polygon_to_search_for_error_in_id_platform_name(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API создания полигона с отсутствием платформы
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id_platform_name": 0,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
    }
    data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/create_polygon_to_search_for", json=data,
    )
    assert response.status_code == 404


def test_create_polygon_to_search_for_error_in_id_polygon_type(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API создания полигона с отсутствием платформы
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id_platform_name": platform.id,
        "id_polygon_type": 0,
        "id_space_program": space_program.id,
    }
    data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/create_polygon_to_search_for", json=data,
    )
    assert response.status_code == 404


def test_create_polygon_to_search_for_error_in_id_space_program(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API создания полигона с отсутствием платформы
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": 0,
    }
    data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/create_polygon_to_search_for", json=data,
    )
    assert response.status_code == 404


def test_create_polygon_to_search_for_error_in_footprint(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API создания полигона с отсутствием платформы
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
        "footprint": "string"
    }
    data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/create_polygon_to_search_for", json=data,
    )
    assert response.status_code == 404
