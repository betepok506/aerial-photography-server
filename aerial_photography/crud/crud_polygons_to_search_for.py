from typing import List
from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.polygons_to_search_for import PolygonsToSearchFor
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate,
    PolygonsToSearchForUpdate,
    PolygonsToSearchForSearch)
from aerial_photography.models.platform_name_sentinel import PlatformNameSentinel
from aerial_photography.utils.geometry import convert_str_to_wkb, convert_wkb_to_str
from geoalchemy2.elements import WKBElement


class CRUDPolygonsToSearchFor(
    CRUDBase[PolygonsToSearchFor, PolygonsToSearchForCreate, PolygonsToSearchForUpdate]):
    '''
    Класс, реализующий функционал CRUD для таблицы `polygons_to_search_for`
    '''

    def create(self, db: Session, *, obj_in: PolygonsToSearchForCreate) -> PolygonsToSearchFor:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['footprint'] = convert_str_to_wkb(obj_in_data['footprint'])

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: PolygonsToSearchFor,
            obj_in: PolygonsToSearchForUpdate
    ) -> PolygonsToSearchFor:
        if isinstance(db_obj.footprint, WKBElement):
            db_obj.footprint = convert_wkb_to_str(db_obj.footprint)

        obj_data = jsonable_encoder(db_obj)
        obj_in.footprint = convert_str_to_wkb(obj_in.footprint)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search(self, db: Session, *, obj_in: PolygonsToSearchForSearch) -> List[PolygonsToSearchFor]:
        result = db.scalars(
            select(PolygonsToSearchFor).where(and_(PolygonsToSearchFor.id_platform_name == PlatformNameSentinel.id,
                                                   PlatformNameSentinel.name == obj_in.platform_name)))
        return [item for item in result]


polygons_to_search_for = CRUDPolygonsToSearchFor(PolygonsToSearchFor)
