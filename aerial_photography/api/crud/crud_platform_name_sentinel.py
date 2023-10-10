from typing import List, Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.api.crud.base import CRUDBase
from aerial_photography.models.platform_name_sentinel import PlatformNameSentinel
from aerial_photography.api.schemas.platform_name_sentinel import \
    PlatformNameSentinelCreate, PlatformNameSentinelSearchById, PlatformNameSentinelSearch


class CRUDPlatformNameSentinel(
    CRUDBase[PlatformNameSentinel, PlatformNameSentinelCreate, PlatformNameSentinelSearchById]):
    # async def create(self, db: Session, *, obj_in: PlatformNameSentinelCreate) -> PlatformNameSentinel:
    #     db_obj = PlatformNameSentinel(name=obj_in.name)
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    async def search(self, db: AsyncSession, *, obj_in: PlatformNameSentinelSearch) -> List[PlatformNameSentinel]:
        # return db.query(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name).all()
        result = await db.scalars(select(PlatformNameSentinel).where(PlatformNameSentinel.name == obj_in.name))
        return [item for item in result]


    # def get(self, db: Session, id: Any) -> PlatformNameSentinel:
    #     return db.query(PlatformNameSentinel).where(PlatformNameSentinel.id == id)

    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: ModelType,
    #     obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    # ) -> ModelType:
    #     pass

    # def remove(self, db: Session, *, id: int) -> ModelType:
    #     pass

    # def create_with_owner(
    #     self, db: Session, *, obj_in: ItemCreate, owner_id: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_id=owner_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj
    #
    # def get_multi_by_owner(
    #     self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Item]:
    #     return (
    #         db.query(self.model)
    #         .filter(Item.owner_id == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


platform_name_sentinel = CRUDPlatformNameSentinel(PlatformNameSentinel)
