# from collections.abc import AsyncGenerator
#
# from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from sqlalchemy import MetaData
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from aerial_photography.config import settings

# Base: DeclarativeMeta = declarative_base()

# engine = create_async_engine(settings.DATABASE_URL)

# ======== Sync ============

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ======== Async ============
# engine = create_async_engine(settings.DATABASE_URL,  pool_pre_ping=True)
# SessionLocal = async_sessionmaker(autocommit=False, autoflush=False,bind=engine, class_=AsyncSession)

# ======== End ============


# metadata = MetaData()
# Base = declarative_base(metadata=metadata)
# print('Create engine')
#
#
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     engine = create_async_engine(settings.DATABASE_URL)
#     factory = async_sessionmaker(engine)
#     async with factory() as session:
#         try:
#             yield session
#             await session.commit()
#         except exc.SQLAlchemyError:
#             await session.rollback()
#             raise
# async def create_db_and_tables():
#     engine = get_db_session()
#     # async with engine.begin() as conn:
#     #     await conn.run_sync(Base.metadata.create_all)
#
#     async with engine as conn:
#         await conn.run_sync(Base.metadata.create_all)
