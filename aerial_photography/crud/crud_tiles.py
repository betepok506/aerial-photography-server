from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.tiles import Tiles
from aerial_photography.schemas.tiles import \
    TilesCreateSchema, TilesUpdateSchema


class CRUDActionType(
    CRUDBase[Tiles, TilesCreateSchema, TilesUpdateSchema]):
    # def search(self, db: Session, *, obj_in: Tiles) -> List[Tiles]:
    #     result = db.scalars(select(ActionType).where(ActionType.name == obj_in.name))
    #     return [item for item in result]
    def get_tiles_by_coordinates(self, db: Session, x: int, y: int, z: int):
        queries = list()
        queries.append(Tiles.x == x)
        queries.append(Tiles.y == y)
        queries.append(Tiles.z == z)

        result = db.scalars(select(Tiles).where(*queries).limit(1))
        result = [item for item in result]
        if len(result) == 0:
            return None

        return result[0]

        pass

    def create(self, db: Session, *, db_obj: Tiles) -> Tiles:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


tiles = CRUDActionType(Tiles)
