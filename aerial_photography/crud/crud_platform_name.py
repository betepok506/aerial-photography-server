from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.platform_name import PlatformName
from aerial_photography.schemas.platform_name import \
    PlatformNameCreate, PlatformNameSearchById, PlatformNameSearch


class CRUDPlatformName(
    CRUDBase[PlatformName, PlatformNameCreate, PlatformNameSearchById]):
    def search(self, db: Session, *, obj_in: PlatformNameSearch) -> List[PlatformName]:
        # return db.query(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name).all()
        result = db.scalars(select(PlatformName).where(PlatformName.name == obj_in.name))
        return [item for item in result]


platform_name = CRUDPlatformName(PlatformName)
