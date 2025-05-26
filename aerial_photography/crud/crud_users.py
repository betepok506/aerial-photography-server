from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from aerial_photography.crud.base import CRUDBase
from aerial_photography.models.users import Users
from aerial_photography.schemas.users import \
    UserCreateSchema, UserUpdateSchema


class CRUDUser(
    CRUDBase[Users, UserCreateSchema, UserUpdateSchema]):
    # def search(self, db: Session, *, obj_in: Tiles) -> List[Tiles]:
    #     result = db.scalars(select(ActionType).where(ActionType.name == obj_in.name))
    #     return [item for item in result]

    def get_user_by_login(self, db: Session, login: str):
        queries = list()
        queries.append(Users.login == login)

        result = db.scalars(select(Users).where(*queries).limit(1))
        result = [item for item in result]
        if len(result) == 0:
            return None

        return result[0]

        pass


user = CRUDUser(Users)
