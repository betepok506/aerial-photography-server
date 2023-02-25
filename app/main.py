import uvicorn

from database import models
from fastapi import FastAPI, Response
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon
from sqlalchemy import create_engine, Column, Integer, func
from fastapi.middleware.cors import CORSMiddleware
from database.models import (
    PoiPolygon,
    ClassObjectDisplay,
    Maps,
    Tiles,
    NeuralNetwork,
    DetectedObjects
)
from database.db import engine
from sqlalchemy.orm import sessionmaker
from shapely import wkb
from app.globalmaptiles import GlobalMercator
from app.schemas import (
    RequestPolygonsObject,
    Tiles_schemas,
    Tile,
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
    db.add(Maps(name=map_info.map_name,
                md5=map_info.hash_md5))
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


@app.post("/add_tiles/")
def add_tiles(tiles: Tiles_schemas):
    # TODO: Добавить в таблицу Maps счетчик tiles для восстановления добавления
    tiles_array = []
    for tile in tiles.tiles:
        tiles_array.append({"map_id": tile["map_id"],
                            "x": tile["x"],
                            "y": tile["y"],
                            "z": tile["z"]})

    db.bulk_insert_mappings(Tiles, tiles_array)

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
