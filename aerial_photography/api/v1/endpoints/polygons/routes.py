import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from shapely import geometry
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from aerial_photography.api.schemas import polygon
from aerial_photography.database import models as db_models
# from aerial_photography.database.session import get_db_session
#
# router = APIRouter(prefix="/v1", tags=["v1"])
#
#
# @router.post("/add_polygon_to_upload", status_code=status.HTTP_200_OK)
# async def add_polygon_to_upload(
#         data: polygon.PolygonToUpload,
#         session: AsyncSession = Depends(get_db_session)
# ):
#     '''
#     Данный метод служит для добавления полигонов для последующего поиска и загрузки
#     '''
#
#     data = data.model_dump()
#
#     poly = geometry.Polygon([[44.680385, 54.721345],
#                              [46.226831, 54.781341],
#                              [46.306982, 53.698870],
#                              [44.392784, 53.779930]])
#
#     employee = db_models.PolygonsToSearchFor(first_name=data['first_name'],
#                                    last_name=data['last_name'],
#                                    patronymic=data['patronymic'],
#                                    image=result_img)
#
#     print(data)
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder({"detail": "The employee has been added successfully!"}),
#     )
