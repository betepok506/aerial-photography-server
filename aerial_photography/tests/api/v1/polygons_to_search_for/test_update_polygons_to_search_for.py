from fastapi.testclient import TestClient
from aerial_photography.config import settings
from sqlalchemy.orm import Session
from aerial_photography.tests.api.v1.polygons_to_search_for.utils import creating_dependent_records, \
    update_template_data, DATA, UPDATED_COORD
from aerial_photography.utils.geometry import convert_polygon_to_str


def test_update_polygon_to_search_for(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона
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

    platform, type_polygon, space_program = creating_dependent_records(db)
    new_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_data = {
        "id": int(content["id"]),
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
        "footprint": new_polygon
    }
    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )

    assert response.status_code == 200

    content = response.json()
    assert content["id_platform_name"] == updated_data["id_platform_name"]
    assert content["id_polygon_type"] == updated_data["id_polygon_type"]
    assert content["id_space_program"] == updated_data["id_space_program"]
    assert content["footprint"] == new_polygon
    assert content["current_downloaded"] == updated_data["current_downloaded"]
    assert content["need_to_download"] == updated_data["need_to_download"]
    assert content["id"] == updated_data["id"]


def test_update_polygon_to_search_for_error_not_found(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
    '''
    platform, type_polygon, space_program = creating_dependent_records(db)
    new_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_data = {
        "id": 0,
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
        "footprint": new_polygon
    }

    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )
    assert response.status_code == 404


def test_update_polygon_to_search_for_error_in_id_platform_name(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
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

    platform, type_polygon, space_program = creating_dependent_records(db)
    new_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_data = {
        "id": content["id"],
        "id_platform_name": 0,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
        "footprint": new_polygon
    }

    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )
    assert response.status_code == 404


def test_update_polygon_to_search_for_error_in_id_polygon_type(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
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

    platform, type_polygon, space_program = creating_dependent_records(db)
    new_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_data = {
        "id": content["id"],
        "id_platform_name": platform.id,
        "id_polygon_type": 0,
        "id_space_program": space_program.id,
        "footprint": new_polygon
    }

    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )
    assert response.status_code == 404


def test_update_polygon_to_search_for_error_in_id_space_program(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
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

    platform, type_polygon, space_program = creating_dependent_records(db)
    new_polygon = convert_polygon_to_str(UPDATED_COORD)
    updated_data = {
        "id": content["id"],
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": 0,
        "footprint": new_polygon
    }

    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )
    assert response.status_code == 404


def test_update_polygon_to_search_for_error_in_footprint(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
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

    platform, type_polygon, space_program = creating_dependent_records(db)
    updated_data = {
        "id": content["id"],
        "id_platform_name": platform.id,
        "id_polygon_type": type_polygon.id,
        "id_space_program": space_program.id,
        "footprint": "string"
    }

    updated_data = update_template_data(DATA, updated_data)
    response = client.post(
        f"{settings.API_V1_STR}/polygon/update_polygon_to_search_for", json=updated_data,
    )
    assert response.status_code == 404
