from collections.abc import AsyncGenerator
from typing import Generator
from aerial_photography.database.session import SessionLocal
from sqlalchemy import exc
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# ===== Async =====
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     # engine = create_async_engine(settings.DATABASE_URL)
#     factory = SessionLocal()
#     async with factory() as session:
#         try:
#             yield session
#             await session.commit()
#         except exc.SQLAlchemyError:
#             await session.rollback()
#             raise


def get_db_session() -> Generator:
    # engine = create_async_engine(settings.DATABASE_URL)
    factory = SessionLocal()
    try:
        yield factory
        factory.commit()
    except exc.SQLAlchemyError:
        factory.rollback()
        raise
    finally:
        factory.close()
