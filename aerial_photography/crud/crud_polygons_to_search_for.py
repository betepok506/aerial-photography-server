from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.polygons_to_search_for import PolygonsToSearchFor
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate,
    PolygonsToSearchForUpdate,
    PolygonsToSearchForSearch)


class CRUDPolygonsToSearchFor(
    CRUDBase[PolygonsToSearchFor, PolygonsToSearchForCreate, PolygonsToSearchForUpdate]):
    '''
    Класс, реализующий функционал CRUD для таблицы `polygons_to_search_for`
    '''

    async def search(self, db: AsyncSession, *, obj_in: PolygonsToSearchForSearch) -> List[PolygonsToSearchFor]:
        # return db.query(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name).all()
        result = await db.scalars(
            select(PolygonsToSearchFor).where(PolygonsToSearchFor.platform_name == obj_in.platform_name))
        return [item for item in result]


polygons_to_search_for = CRUDPolygonsToSearchFor(PolygonsToSearchFor)
