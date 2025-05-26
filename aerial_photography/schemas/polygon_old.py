# from typing import Union, Iterable, List
# from datetime import datetime
# from pydantic import BaseModel
#
#
# class PolygonToUpload(BaseModel):
#     '''
#     Схема для добавления информации о полигонов в базу для последующего запроса снимков внитру этих полигонов
#     '''
#     polygon: str
#     platform_name: int or str
#     collection: int or str
#     date_from: datetime or None
#     date_to: datetime or None
#     type_polygon: int
