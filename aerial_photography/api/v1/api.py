from fastapi import APIRouter

from aerial_photography.api.v1.endpoints import polygon_to_search_for, images

api_router = APIRouter()
api_router.include_router(polygon_to_search_for.router, prefix="/polygon", tags=["polygon"])
api_router.include_router(images.router, prefix="/image", tags=["image"])
