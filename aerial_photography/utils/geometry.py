'''
Данный модуль содержит вспомогательные функции для работы с геометрией
'''
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon
from typing import List, Tuple


def convert_wkb(polygon_coordinates: List[Tuple[float, float]]):
    '''
    Функция производит преобразование географических координат в wkb формат

    Parameter
    ----------
    polygon_coordinates: `List[List[int, int]]`
        Массив координат полигона

    Returns
    ----------
        `str` полигон, преобразованный в wkb формат
    '''
    polygon = Polygon(polygon_coordinates)
    wkb_format = from_shape(polygon, 4326)
    return wkb_format
