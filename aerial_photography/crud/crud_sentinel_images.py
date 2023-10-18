from typing import List
from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.sentinel_images import SentinelImages
from aerial_photography.schemas.sentinel_images import (
    SentinelImagesCreate,
    SentinelImagesUpdate,
    SentinelImagesSearch)
from aerial_photography.models.platform_name_sentinel import PlatformNameSentinel
from aerial_photography.utils.geometry import convert_str_to_wkb, convert_wkb_to_str
from geoalchemy2.elements import WKBElement


class CRUDSentinelImages(
    CRUDBase[SentinelImages, SentinelImagesCreate, SentinelImagesUpdate]):
    '''
    Класс, реализующий функционал CRUD для таблицы `sentinel_images`
    '''

    def create(self, db: Session, *, obj_in: SentinelImagesCreate) -> SentinelImages:
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
            db_obj: SentinelImages,
            obj_in: SentinelImagesUpdate
    ) -> SentinelImages:
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

    def search(self, db: Session, *, obj_in: SentinelImagesSearch) -> List[SentinelImages]:
        result = db.scalars(
            select(SentinelImages).where(and_(SentinelImages.platform_id == PlatformNameSentinel.id,
                                              PlatformNameSentinel.name == obj_in.platform_name)))
        return [item for item in result]


sentinel_images = CRUDSentinelImages(SentinelImages)
