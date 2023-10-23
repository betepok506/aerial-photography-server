from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from shapely.errors import GEOSException
from sqlalchemy.exc import IntegrityError
from aerial_photography.api.deps import get_db_session
from aerial_photography import schemas
from aerial_photography import crud

router = APIRouter()


@router.post("/create_polygon_to_search_for")
def create_polygon_to_search_for(
        *,
        db: Session = Depends(get_db_session),
        polygon_in: schemas.PolygonsToSearchForCreate
):
    '''
    "POLYGON ((44.680385 54.721345, 46.226831 54.781341, 46.306982 53.69887, 44.392784 53.77993, 44.680385 54.721345))"
    '''
    try:
        polygon = crud.polygons_to_search_for.create(db=db, obj_in=polygon_in)
    except IntegrityError as foreign_key_exception:
        raise HTTPException(status_code=404, detail="The element being created refers to a non-existent element!")
    except GEOSException as parse_exception:
        raise HTTPException(status_code=404, detail="The coordinates of the polygon are incorrectly specified!")

    return polygon


@router.delete("/delete_polygon_to_search_for/{id}")
def delete_polygon_to_search_for(
        *,
        db: Session = Depends(get_db_session),
        id: int
):
    removed_polygon = crud.polygons_to_search_for.remove(db=db, id=id)
    if not removed_polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    return removed_polygon


@router.post("/update_polygon_to_search_for")
def update_polygon_to_search_for(
        *,
        db: Session = Depends(get_db_session),
        polygon_in: schemas.PolygonsToSearchForUpdate
):
    polygon = crud.polygons_to_search_for.get(db=db, id=polygon_in.id)
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    try:
        updated_polygon = crud.polygons_to_search_for.update(db=db, db_obj=polygon, obj_in=polygon_in)
    except IntegrityError as foreign_key_exception:
        raise HTTPException(status_code=404, detail="The element being updated refers to a non-existent element!")
    except GEOSException as parse_exception:
        raise HTTPException(status_code=404, detail="The coordinates of the polygon are incorrectly specified!")

    return updated_polygon


@router.get("/get_polygon_to_search_for/{id}")
def get_polygon_to_search_for(
        *,
        db: Session = Depends(get_db_session),
        id: int
):
    polygon = crud.polygons_to_search_for.get(db=db, id=id)
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    return polygon


@router.get("/get_polygons_to_search_for")
def get_polygons_to_search_for(
        *,
        db: Session = Depends(get_db_session),
        skip: int = 0,
        limit: int = 100
):
    polygons = crud.polygons_to_search_for.get_multi(db=db, skip=skip, limit=limit)
    if not polygons:
        raise HTTPException(status_code=404, detail="Polygon not found")

    return polygons
