from sqlalchemy.orm import Session
from aerial_photography.database import base
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from aerial_photography.database.base_class import Base
# from aerial_photography.database.session import engine


async def create_db_and_tables(session: Session):
    engine = session.get_bind()
    Base.metadata.create_all(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
