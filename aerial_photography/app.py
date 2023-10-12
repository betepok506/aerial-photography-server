from fastapi import FastAPI
import uvicorn
# from aerial_photography.api.v1.polygons.routes import router as v1_router
# from aerial_photography.api.v2.routes import router as v2_router
from aerial_photography.config import settings
from aerial_photography.utils.initial_default_db import (
    initial_table_platform_name_sentinel,
    initial_table_type_polygons_to_search_for)
from aerial_photography.database.base_class import Base
from aerial_photography.database.session import engine, SessionLocal


# from aerial_photography.database.models import (
#     PoiPolygon,
#     ClassObjectDisplay,
#     Maps,
#     Tiles,
#     PlatformNameSentinel
# )

# engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
# SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# @event.listens_for(PlatformNameSentinel.__table__, 'after_create')
# def insert_initial_values(target,
#                           connection: AsyncSession = Depends(get_db_session),
#                           **kwargs):
#     print(f' {target}')
#     connection.execute(insert(PlatformNameSentinel.__table__).values(name="low"))
#     connection.execute(insert(PlatformNameSentinel.__table__).values(name="medium"))
#     connection.execute(insert(PlatformNameSentinel.__table__).values(name="Morro Bay"))
#     # connection.commit()
#     # connection.close()
#     print("insert_initial_values success calling db func: ")


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


# app.include_router(v1_router, prefix="/api")
# aerial_photography.include_router(v2_router, prefix="/api")

@app.on_event("startup")
async def initial_db():
    session = SessionLocal()
    await create_db_and_tables()
    await initial_table_platform_name_sentinel(session)
    await initial_table_type_polygons_to_search_for(session)
    # await crud.platform_name_sentinel.create(db=session, obj_in=schemas.PlatformNameSentinelCreate(name='test_create2'))
    # print(await crud.platform_name_sentinel.get(db=session, id=1))
    # tt = await crud.platform_name_sentinel.get(db=session, id=7)
    # print(await crud.platform_name_sentinel.remove(db=session, id=1))

    # await crud.platform_name_sentinel.update(db=session,
    #                                          db_obj=tt,
    #                                          obj_in=schemas.PlatformNameSentinel(name='gg'))

    print('Initialization completed successfully!')
    # models.Base.metadata.create_all(bind=engine)

# TODO: Добавить реконнект в случае ошибки с базой через retry
# TODO: Добавить закрытие соединения после завершения транзакции

if __name__ == "__main__":
    uvicorn.run("aerial_photography.app:app", port=8001, log_level="info", reload=True)
