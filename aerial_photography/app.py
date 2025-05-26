from fastapi import FastAPI
import uvicorn
# from aerial_photography.api.v1.polygons.routes import router as v1_router
# from aerial_photography.api.v2.routes import router as v2_router
from aerial_photography.config import settings
from aerial_photography.utils.initial_default_db import (
    initial_table_platform_name_sentinel,
    initial_table_type_polygons_to_search_for,
    initial_table_space_programs
)
from aerial_photography.api.v1.api import api_router
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

# ======== Async ============
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# ======== Sync ============
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def initial_db():
    session = SessionLocal()
    create_db_and_tables()
    initial_table_platform_name_sentinel(session)
    initial_table_type_polygons_to_search_for(session)
    initial_table_space_programs(session)


# TODO: Добавить реконнект в случае ошибки с базой через retry
# TODO: Добавить закрытие соединения после завершения транзакции

# if __name__ == "__main__":
#     uvicorn.run("aerial_photography.app:app", port=8001, log_level="info", reload=True)
