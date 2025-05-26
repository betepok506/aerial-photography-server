from typing import List, Union
from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from aerial_photography.crud.base import CRUDBase
from sqlalchemy import func
from aerial_photography.models.polygons_to_search_for import PolygonsToSearchFor
from aerial_photography.schemas.polygons_to_search_for import (
    PolygonsToSearchForCreate,
    PolygonsToSearchForUpdate)
# PolygonsToSearchForSearch,
# PolygonsToSearchForSearchByPrograms)
from aerial_photography.models.platform_name import PlatformName
from aerial_photography.models.space_programs import SpacePrograms
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
        # TODO: Разобраться почему с этой строчкой не работаю тесты
        db_obj.footprint = convert_wkb_to_str(db_obj.footprint)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: PolygonsToSearchFor,
            obj_in: PolygonsToSearchForUpdate
    ) -> PolygonsToSearchFor:
        # Проверка корректности переданного полигона
        # convert_wkb_to_str(db_obj.footprint)
        obj_data = jsonable_encoder(db_obj)
        # obj_in.footprint = convert_str_to_wkb(obj_in.footprint)
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

        if isinstance(db_obj.footprint, WKBElement):
            db_obj.footprint = convert_wkb_to_str(db_obj.footprint)

        return db_obj

    def get(self, db: Session, id: int) -> Union[PolygonsToSearchFor, None]:
        result = db.scalars(select(self.model).filter(self.model.id == id).limit(1))
        result = [item for item in result]
        if len(result) == 0:
            return None

        if isinstance(result[0].footprint, WKBElement):
            result[0].footprint = convert_wkb_to_str(result[0].footprint)

        return result[0]

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[PolygonsToSearchFor]:
        result = db.scalars(select(self.model).offset(skip).limit(limit))
        result = [item for item in result]
        for ind in range(len(result)):
            result[ind].footprint = convert_wkb_to_str(result[ind].footprint)

        return result

    def remove(self, db: Session, *, id: int) -> Union[PolygonsToSearchFor, None]:
        obj = self.get(db=db, id=id)
        if obj is None:
            return None

        db.delete(obj)
        db.commit()
        return obj

    def get_count(self, db: Session):
        counts = db.query(func.count(self.model.id)).scalar()
        return counts


polygons_to_search_for = CRUDPolygonsToSearchFor(PolygonsToSearchFor)
