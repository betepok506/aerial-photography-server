from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.space_programs import SpacePrograms
from aerial_photography.schemas.space_programs import \
    SpaceProgramsCreate, SpaceProgramsUpdate, SpaceProgramsSearchById, SpaceProgramsSearch


class CRUDSpacePrograms(
    CRUDBase[SpacePrograms, SpaceProgramsCreate, SpaceProgramsSearchById]):
    def search(self, db: Session, *, obj_in: SpaceProgramsSearch) -> List[SpacePrograms]:
        result = db.scalars(select(SpacePrograms).where(SpacePrograms.name == obj_in.name))
        return [item for item in result]


space_programs = CRUDSpacePrograms(SpacePrograms)
