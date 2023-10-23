from fastapi import APIRouter

from aerial_photography.api.v1.endpoints import polygon_to_search_for

api_router = APIRouter()
api_router.include_router(polygon_to_search_for.router, prefix="/polygon", tags=["polygon"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
