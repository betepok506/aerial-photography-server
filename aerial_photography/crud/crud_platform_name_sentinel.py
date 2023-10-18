from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.platform_name_sentinel import PlatformNameSentinel
from aerial_photography.schemas.platform_name_sentinel import \
    PlatformNameSentinelCreate, PlatformNameSentinelSearchById, PlatformNameSentinelSearch


class CRUDPlatformNameSentinel(
    CRUDBase[PlatformNameSentinel, PlatformNameSentinelCreate, PlatformNameSentinelSearchById]):
    def search(self, db: Session, *, obj_in: PlatformNameSentinelSearch) -> List[PlatformNameSentinel]:
        # return db.query(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name).all()
        result = db.scalars(select(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name))
        return [item for item in result]


platform_name_sentinel = CRUDPlatformNameSentinel(PlatformNameSentinel)
