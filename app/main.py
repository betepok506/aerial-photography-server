import base64

import uvicorn

from database import models
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response, StreamingResponse
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon
import json
from sqlalchemy import create_engine, Column, Integer, func, and_, tuple_
from fastapi.middleware.cors import CORSMiddleware
from database.models import (
    PoiPolygon,
    ClassObjectDisplay,
    Maps,
    Tiles,
    NeuralNetwork,
    DetectedObjects
)
import numpy as np
import io
from PIL import Image

from database.db import engine
from sqlalchemy.orm import sessionmaker
from shapely import wkb
from app.globalmaptiles import GlobalMercator
from app.schemas import (
    RequestPolygonsObject,
    TilesSchemas,
    Tile,
    RequestsRawTiles,
    MapInfo
)

models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db = Session()

app = FastAPI()


def db_persist(func):
    def persist(*args, **kwargs):
        func(*args, **kwargs)
        try:
            Session.commit()
            print("success calling db func: " + func.__name__)
            # logger.info("success calling db func: " + func.__name__)
            return True
        except SQLAlchemyError as e:
            # logger.error(e.args)
            print(e.args)
            Session.rollback()
            return False
        finally:
            Session.close()

    return persist


@app.get("/get_bbox_object/")
def get_bbox_object(z: int, x: int, y: int):
    # if z < 19:
    #     return []
    # bounds = []
    # return bounds

    glm = GlobalMercator()
    coords = list(map(abs, glm.TileLatLonBounds(x, y, z)))
    # coords = [coords[1], coords[0], coords[3], coords[2]]
    coords = [coords[1], coords[0], coords[3], coords[2]]

    polygon = Polygon([
        [coords[0], coords[1]],
        [coords[0], coords[3]],
        [coords[2], coords[3]],
        [coords[2], coords[1]],
        [coords[0], coords[1]]
    ])

    return polygon_query_db(polygon)


@app.get("/classes_query/")
def classes_query_db():
    """
    Запрос классов объектов

    Returns
    -----------
    `list`
        Классы объектов для отображения
    """
    query = db.query(ClassObjectDisplay).all()
    return query


@app.get("/query_hash_md5_map/{map_name}")
def query_hash_md5_map(map_name: str):
    """
    Запрос md5 хеша карты по ее имени

    Parameters
    -----------
    map_name: `str`
        Название карты

    Returns
    -----------
    `str`
        Md5 хеш карты
    """
    query = db.query(Maps).filter(Maps.name == map_name).first()
    # Todo: Протестировать когда возвращается пустой запрос
    if query is None:
        return {}

    return {
        "map_id": query.id,
        "hash_md5": query.md5
    }


@app.post("/add_map/")
def add_map(map_info: MapInfo):
    # map_info = map_info.dict()
    query = db.query(Maps).filter(Maps.name == map_info.map_name)

    db.add(Maps(name=map_info.map_name))
    try:
        db.commit()
        print("success calling db func: ")
        # logger.info("success calling db func: " + func.__name__)
    except SQLAlchemyError as e:
        # logger.error(e.args)
        print(e.args)
        db.rollback()
        return Response(
            status_code=500,
            content="Failed to add map data to the database."
        )
    finally:
        db.close()

    return query_hash_md5_map(map_info.map_name)


def merge_tiles(tiles_upgrade, tiles_added):
    '''
    Функция для объединения изображений плиток

    # TODO: Добавить порядок мержа в зависимости от времени добавления плиток
    '''
    for ind in range(len(tiles_added)):
        result_image = merge_image(Image.open(io.BytesIO(base64.b64decode(tiles_upgrade[ind]["image"]))),
                                   Image.open(io.BytesIO(base64.b64decode(tiles_added[ind]["image"]))))
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        result_im_b64 = base64.b64encode(img_byte_arr).decode("utf8")

        tiles_added[ind]["image"] = result_im_b64.encode("utf-8")

    return tiles_added


def merge_image(img1, img2):
    f_img_array = np.asarray(img1)
    s_img_array = np.asarray(img2)

    newImArray = np.empty(f_img_array.shape, dtype='uint8')
    for row in range(f_img_array.shape[0]):
        for col in range(f_img_array.shape[1]):
            if not (np.array_equal(f_img_array[row][col], [0, 0, 0, 0]) or \
                    np.array_equal(f_img_array[row][col], [0, 0, 0, 255])):
                newImArray[row][col] = f_img_array[row][col]

            elif not (np.array_equal(s_img_array[row][col], [0, 0, 0, 0]) or \
                      np.array_equal(s_img_array[row][col], [0, 0, 0, 255])):
                newImArray[row][col] = s_img_array[row][col]
            else:
                newImArray[row][col] = [0, 0, 0, 0]

    result = Image.fromarray(newImArray, "RGBA")
    return result


def clear_background(img):
    img_array = np.asarray(img)
    newImArray = np.empty(img_array.shape, dtype='uint8')
    # mask = (img_array[:, :] == np.array([0, 0, 0, 255]))
    # mask = np.all(img_array == (0, 0, 0, 255), axis=0)
    mask = np.logical_and.reduce((img_array[:, :, 0] == 0,
                                  img_array[:, :, 1] == 0,
                                  img_array[:, :, 2] == 0,
                                  img_array[:, :, 3] == 255))
    newImArray = img_array.copy()
    newImArray[mask] = [0, 0, 0, 0]

    result = Image.fromarray(newImArray, "RGBA")
    return result


@app.post("/add_tiles/")
def add_tiles(tiles: TilesSchemas):
    # TODO: Добавить в таблицу Maps счетчик tiles для восстановления добавления

    # Находим новые карты, которые встречаются в плитках
    unique_input_map_name = set()
    for tile in tiles.tiles:
        unique_input_map_name.add(tile.map_name)

    mapsname2mapsid = {}
    # Запрашиваем карты в бд, возвращает найденные
    query = db.query(Maps).filter(Maps.name.in_(list(unique_input_map_name))).all()
    unique_found_maps = set()
    for cur_map_name in query:
        mapsname2mapsid[cur_map_name.name] = cur_map_name.id
        unique_found_maps.add(cur_map_name.name)

    # Находим карты, которые отсутствуют в БД
    unique_new_maps = unique_input_map_name.difference(unique_found_maps)
    # Добавляем их в БД
    added_maps = []
    for cur_map_name in unique_new_maps:
        added_maps.append(Maps(name=cur_map_name))

    db.add_all(added_maps)
    db.commit()

    # Запрашиваем карты, для привязки в id
    map_name2map_id = {}
    query = db.query(Maps).filter(Maps.name.in_(list(unique_input_map_name))).all()
    for cur_map in query:
        map_name2map_id[cur_map.name] = cur_map.id

    coords = []
    for tile in tiles.tiles:
        coords.append([mapsname2mapsid[tile.map_name], tile.x, tile.y, tile.z])

    query_tiles_added = db.query(Tiles).where(tuple_(Tiles.map_id, Tiles.x, Tiles.y, Tiles.z).in_(coords)).all()
    tiles_upgrade = []
    tiles_added = []
    # Смержить все, что нашел в query
    new_tiles_array = []
    # TODO: Сделал топорную проверку была ли добавлена плитки Позже переписать
    # todo: Декомпозировать и универсализировать функцию
    for tile in tiles.tiles:
        for tile_added in query_tiles_added:
            if tile.x == tile_added.x and \
                    tile.y == tile_added.y and \
                    tile.z == tile_added.z:
                tiles_upgrade.append({
                    "map_id": map_name2map_id[tile.map_name],
                    "image": tile.image,
                    "x": tile.x,
                    "y": tile.y,
                    "z": tile.z})

                tiles_added.append({
                    "id": tile_added.id,
                    "map_id": map_name2map_id[tile.map_name],
                    "image": tile_added.image,
                    "x": tile_added.x,
                    "y": tile_added.y,
                    "z": tile_added.z})

                break
        else:
            clear_image = clear_background(Image.open(io.BytesIO(base64.b64decode(tile.image))))
            img_byte_arr = io.BytesIO()
            clear_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            result_im_b64 = base64.b64encode(img_byte_arr).decode("utf8")

            new_tiles_array.append({
                "map_id": map_name2map_id[tile.map_name],
                "image": result_im_b64.encode("utf-8"),
                "x": tile.x,
                "y": tile.y,
                "z": tile.z})

    '''
    ++++++++++++++++++++++++++++++++++
            Обновление элементов
    ++++++++++++++++++++++++++++++++++
    '''
    tiles_upgrade = merge_tiles(tiles_upgrade, tiles_added)

    db.bulk_update_mappings(Tiles, tiles_upgrade)
    # Множественное добавление плиток
    db.bulk_insert_mappings(Tiles, new_tiles_array)

    try:
        db.commit()
        print("success calling db func: ")
        # logger.info("success calling db func: " + func.__name__)
        return True
    except SQLAlchemyError as e:
        # logger.error(e.args)
        print(e.args)
        db.rollback()
        return False
    finally:
        db.close()


@app.get("/get_tiles/")
def get_tiles(z: int, x: int, y: int):
    # from io import BytesIO
    # import os
    # import io
    # from PIL import Image
    #
    # img = Image.open("D:\\diploma_project\\aerial_photo_processing_service\data\\tilesdir\\3\\4\\1.png", mode='r')
    # img_byte_arr = io.BytesIO()
    # img.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()
    # sttt = img_byte_arr.decode("utf-8")

    #
    # with open(os.path.join(path_to_tiles, zoom, y, x), "rb") as f:
    #     im_bytes = f.read()
    #
    # im_b64 = base64.b64encode(img_byte_arr)
    # base64_encoded_result_bytes = base64.b64encode(img_byte_arr)
    # base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
    # base64_decoded = str.encode(base64_encoded_result_str, 'ascii')
    # base64_decoded = base64.decodebytes(base64_encoded_result_bytes) # Робит
    #
    # x,y,z = 0,0,0
    query_map_id = db.query(Maps).where(Maps.name == 'landsat8').all()
    query = db.query(Tiles).where(Tiles.map_id == query_map_id[0].id, Tiles.x == x, Tiles.y == y, Tiles.z == z).all()
    # ttt = query[0].image.decode('base64')
    # ttt = base64.decodestring(query[0].image)
    # ttt = query[0].image.decode("utf-8")
    # ttt = BytesIO(query[0].image)
    if len(query):
        # TODO: Добавить затычку если нет изображения
        base64_decoded = base64.decodebytes(query[0].image)
        return Response(
            # content=img_byte_arr, # Робит
            content=base64_decoded,
            media_type='image/png',
            # headers={'Content-Length': str(ttt)}
            # media_type="image/jpeg",
        )
    else:
        return Response(
            content=b'',
            media_type='image/png',
        )


@app.get("/get_fire_tiles/")
def get_fire_tiles(z: int, x: int, y: int):
    query_map_id = db.query(Maps).where(Maps.name == 'fire').all()
    if not len(query_map_id):
        return Response(
            content=b'',
            media_type='image/png',
        )

    query = db.query(Tiles).where(Tiles.map_id == query_map_id[0].id, Tiles.x == x, Tiles.y == y, Tiles.z == z).all()
    if len(query):
        # TODO: Добавить затычку если нет изображения
        base64_decoded = base64.decodebytes(query[0].image)
        return Response(
            # content=img_byte_arr, # Робит
            content=base64_decoded,
            media_type='image/png',
            # headers={'Content-Length': str(ttt)}
            # media_type="image/jpeg",
        )
    else:
        return Response(
            content=b'',
            media_type='image/png',
        )


@app.get("/get_raw_tiles")
def get_raw_tiles(body: RequestsRawTiles):
    maps_query = db.query(Maps).filter(Maps.name == body.map_name).all()
    if not len(maps_query):
        return Response(content="Map not found!")

    query = db.query(Tiles).where(and_(Tiles.map_id == int(maps_query[0].id), Tiles.deleted == False)).limit(body.cnt)
    tiles = []
    tiles_upgrade = []
    for cur_row in query:
        tiles.append({
            "image": base64.b64encode(cur_row.image).decode('utf-8'),
            "x": cur_row.x,
            "y": cur_row.y,
            "z": cur_row.z,
        })
        tiles_upgrade.append({
            "id": cur_row.id,
            'deleted': True
        })
    db.bulk_update_mappings(Tiles, tiles_upgrade)
    try:
        db.commit()
        print("success calling db func: ")
    except SQLAlchemyError as e:
        # logger.error(e.args)
        print(e.args)
        db.rollback()

    finally:
        db.close()

    return Response(
        content=json.dumps({"tiles": tiles})
    )


@app.post("/delete_tiles/")
def delete_tiles():
    pass


@app.get("/update_hash_md5_map/")
def update_hash_md5_map():
    pass


def polygon_query_db(polygon: Polygon):
    """
    Запрос полигонов, пересекающих передаваемый полигон. Polygon представляет набор точек [Lng, Lat].

    Parameters
    ------------
    polygon: `Polygon`
        Передаваемый полигон

    Returns
    ------------
    `list`
        Список полигонов, пересекающих переданный
    """
    wkb_format = from_shape(polygon, 4326)
    query = db.query(PoiPolygon.wkb_geometry).filter(PoiPolygon.wkb_geometry.ST_Intersects(wkb_format)).all()

    bounds = []
    for cur_row in query:
        for wkb_str in cur_row:
            multipolygon = wkb.loads(wkb_str.desc)
            lng, lat = multipolygon.envelope.exterior.coords.xy
            bound = []
            for ind in range(len(lng)):
                bound.append([lat[ind], lng[ind]])

            bounds.append(bound)
    return bounds


@app.post("/polygon_object_by_lat_lng/")
def polygon_object_by_lat_lng(bbox: RequestPolygonsObject):
    """
    Функция для запроса полигонов, лежищих внутри передаваемых координат.
                  _________
    ^            /        /
    | --- Lat   /        /
    |          /        /
              /________/
     ------->  Lng

    Parameters
    ------------
    lat_min: `float`
        Широта левого нижнего угла
    lng_min: `float`
        Долгота левого нижнего угла
    lat_max: `float`
        Широта правого верхнего угла
    lng_max: `float`
        Долгота правого верхнего угла
    cls_obj: `int`
        Запрашиваемый класс объектов

    Returns
    `list`
        Список полигонов, лежащих внутри переданных координат
    ------------
    """
    bbox = bbox.dict()
    polygon = Polygon([
        [bbox["lng_min"], bbox["lat_min"]],
        [bbox["lng_min"], bbox["lat_max"]],
        [bbox["lng_max"], bbox["lat_max"]],
        [bbox["lng_max"], bbox["lat_min"]],
        [bbox["lng_min"], bbox["lat_min"]]
    ])
    return polygon_query_db(polygon)


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, log_level="info", reload=True)
