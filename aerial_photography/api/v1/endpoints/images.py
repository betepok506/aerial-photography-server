from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from shapely.errors import GEOSException
from sqlalchemy.exc import IntegrityError
from aerial_photography.api.deps import get_db_session
from aerial_photography import schemas
from aerial_photography import crud

router = APIRouter()


@router.post("/create_image")
def create_image(
        *,
        db: Session = Depends(get_db_session),
        image_in: schemas.ImagesCreate
):
    image = crud.images.create(db=db, obj_in=image_in)
    return image


@router.delete("/delete_image")
def delete_image(
        *,
        db: Session = Depends(get_db_session),
        id: int
):
    removed_image = crud.images.remove(db=db, id=id)
    if not removed_image:
        raise HTTPException(status_code=404, detail="Image not found")

    return removed_image


@router.post("/update_image")
def update_image(
        *,
        db: Session = Depends(get_db_session),
        image_in: schemas.ImagesUpdate
):
    image = crud.images.get(db=db, id=image_in.id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    updated_image = crud.images.update(db=db, db_obj=image, obj_in=image_in)
    return updated_image


@router.get("/get_image")
def get_image(
        *,
        db: Session = Depends(get_db_session),
        id: int
):
    image = crud.images.get(db=db, id=id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image


@router.get("/get_images")
def get_images(
        *,
        db: Session = Depends(get_db_session),
        skip: int = 0,
        limit: int = 100
):
    images = crud.images.get_multi(db=db, skip=skip, limit=limit)
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")

    return images
