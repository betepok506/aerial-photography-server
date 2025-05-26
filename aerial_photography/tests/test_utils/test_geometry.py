from shapely.geometry import Polygon
from typing import List, Tuple
import shapely
import shapely.wkt
from aerial_photography.utils.geometry import (
    convert_str_to_wkb, convert_wkb_to_str, convert_polygon_to_str)
from geoalchemy2.elements import WKBElement

# Координаты тестового полигона
COORD = [(44.680385, 54.721345),
         (46.226831, 54.781341),
         (46.306982, 53.698870),
         (44.392784, 53.779930)]


def test_convert_polygon_to_str():
    coord = COORD.copy()
    assert coord is not COORD
    converted_polygon = convert_polygon_to_str(coord)
    assert isinstance(converted_polygon, str)
    assert coord == COORD


def test_convert_str_to_wkb():
    coord = COORD.copy()
    assert coord is not COORD
    converted_polygon_str = convert_polygon_to_str(coord)
    converted_polygon = convert_str_to_wkb(converted_polygon_str)
    assert isinstance(converted_polygon, WKBElement)
    assert coord == COORD


def test_convert_wkb_to_str():
    coord = COORD.copy()
    assert coord is not COORD

    converted_polygon_str = convert_polygon_to_str(coord)
    converted_polygon_wkb = convert_str_to_wkb(converted_polygon_str)

    assert isinstance(converted_polygon_wkb, WKBElement)
    reversed_converted_polygon_str = convert_wkb_to_str(converted_polygon_wkb)
    assert converted_polygon_str == reversed_converted_polygon_str
    assert coord == COORD
