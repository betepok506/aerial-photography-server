from typing import List, Union
from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.sentinel_images import Images
from aerial_photography.schemas.images import (
    ImagesCreate,
    ImagesUpdate,
    ImagesSearch)
from aerial_photography.models.platform_name import PlatformName
from aerial_photography.utils.geometry import convert_str_to_wkb, convert_wkb_to_str
from geoalchemy2.elements import WKBElement


class CRUDImages(
    CRUDBase[Images, ImagesCreate, ImagesUpdate]):
    '''
    Класс, реализующий функционал CRUD для таблицы `sentinel_images`
    '''

    def create(self, db: Session, *, obj_in: ImagesCreate) -> Images:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['footprint'] = convert_str_to_wkb(obj_in_data['footprint'])

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        db_obj.footprint = convert_wkb_to_str(db_obj.footprint)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: Images,
            obj_in: ImagesUpdate
    ) -> Images:
        # if isinstance(db_obj.footprint, WKBElement):
        #     db_obj.footprint = convert_wkb_to_str(db_obj.footprint)

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

    def get(self, db: Session, id: int) -> Union[Images, None]:
        result = db.scalars(select(self.model).filter(self.model.id == id).limit(1))
        result = [item for item in result]
        if len(result) == 0:
            return None

        if isinstance(result[0].footprint, WKBElement):
            result[0].footprint = convert_wkb_to_str(result[0].footprint)

        return result[0]

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Images]:
        result = db.scalars(select(self.model).offset(skip).limit(limit))
        result = [item for item in result]
        for ind in range(len(result)):
            result[ind].footprint = convert_wkb_to_str(result[ind].footprint)

        return result

    def search(self, db: Session, *, obj_in: ImagesSearch) -> List[Images]:
        result = db.scalars(
            select(Images).where(and_(Images.id_platform_name == PlatformName.id,
                                      PlatformName.name == obj_in.platform_name)))
        return [item for item in result]

    def intersection(self, db: Session, *, obj_in: ImagesSearch):
        pass



images = CRUDImages(Images)
