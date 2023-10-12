from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from aerial_photography.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)



class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.scalars(select(self.model).filter(self.model.id == id).limit(1))
        result = [item for item in result]
        if len(result) == 0:
            return None
        return result[0]
        # return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        # return db.query(self.model).offset(skip).limit(limit).all()
        result = await db.scalars(select(self.model).offset(skip).limit(limit))
        result = [item for item in result]
        return result

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # json_db_obj = jsonable_encoder(db_obj)
        # json_db_obj.pop('id', None)
        # await db.execute(update(self.model).values(**json_db_obj).filter_by(id=db_obj.id))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Union[ModelType, None]:
        # obj = db.query(self.model).get(id)
        obj = await self.get(db=db, id=id)
        if obj is None:
            return None

        await db.delete(obj)
        await db.commit()
        return obj
