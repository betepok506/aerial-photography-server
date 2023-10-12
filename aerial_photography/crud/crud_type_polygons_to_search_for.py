from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.type_polygon_to_search_for import TypePolygonsToSearchFor
from aerial_photography.schemas.type_polygons_to_search_for import (
    TypePolygonsToSearchForCreate,
    TypePolygonsToSearchForUpdate,
    TypePolygonsToSearchForSearch)


class CRUDTypePolygonsToSearchFor(
    CRUDBase[TypePolygonsToSearchFor,
    TypePolygonsToSearchForCreate,
    TypePolygonsToSearchForUpdate]):
    '''
    Класс, реализующий функционал CRUD для таблицы `type_polygons_to_search_for`
    '''

    async def search(self, db: AsyncSession, *, obj_in: TypePolygonsToSearchForSearch) -> List[TypePolygonsToSearchFor]:
        # return db.query(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name).all()
        result = await db.scalars(
            select(TypePolygonsToSearchFor).where(TypePolygonsToSearchFor.name == obj_in.name))
        return [item for item in result]


type_polygons_to_search_for = CRUDTypePolygonsToSearchFor(TypePolygonsToSearchFor)
