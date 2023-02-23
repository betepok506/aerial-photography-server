import uvicorn

from database import models
from fastapi import FastAPI
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon
from sqlalchemy import create_engine, Column, Integer, func
from fastapi.middleware.cors import CORSMiddleware
from database.models import PoiPolygon, ClassObjectDisplay
from database.db import engine
from sqlalchemy.orm import sessionmaker
from shapely import wkb
from app.globalmaptiles import GlobalMercator
from app.schemas import RequestPolygonsObject

models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db = Session()

app = FastAPI()


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
    query = db.query(ClassObjectDisplay).all()
    return query


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
