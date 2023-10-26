from fastapi.testclient import TestClient
from aerial_photography.config import settings
from sqlalchemy.orm import Session
from aerial_photography.tests.api.v1.polygons_to_search_for.utils import creating_dependent_records, \
    update_template_data, DATA, UPDATED_COORD


def test_get_polygon_to_search_for(
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
    requested_id = content["id"]
    response = client.get(
        f"{settings.API_V1_STR}/polygon/get_polygon_to_search_for/", params={"id": requested_id},
    )
    assert response.status_code == 200

    content = response.json()
    assert content["id_platform_name"] == data["id_platform_name"]
    assert content["id_polygon_type"] == data["id_polygon_type"]
    assert content["id_space_program"] == data["id_space_program"]
    assert content["footprint"] == DATA['footprint']
    assert content["current_downloaded"] == data["current_downloaded"]
    assert content["need_to_download"] == data["need_to_download"]
    assert content["id"] == requested_id


def test_get_polygon_to_search_for_error_not_found(
        client: TestClient, db: Session
) -> None:
    '''
    Функция тестирования API обновления полигона с отсутствием обновляемого полигона
    '''
    response = client.get(
        f"{settings.API_V1_STR}/polygon/get_polygon_to_search_for", params={"id": 0},
    )
    assert response.status_code == 404


# TODO: дОБАВИТЬ Тестирование запросов списка полигонов
# def test_get_polygons_to_search_for(
#         client: TestClient, db: Session
# ) -> None:
#     '''
#     Функция тестирования API обновления полигона
#     '''
#     num_create_polygons = 7
#     for _ in range(num_create_polygons):
#         platform, type_polygon, space_program = creating_dependent_records(db)
#
#     for cur_limit in range(num_create_polygons):
#         for cur_offset in range(num_create_polygons):
#