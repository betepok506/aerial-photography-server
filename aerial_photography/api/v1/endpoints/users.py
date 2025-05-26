from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from shapely.errors import GEOSException
from sqlalchemy.exc import IntegrityError
import base64
from fastapi.responses import FileResponse, Response, StreamingResponse
from aerial_photography.api.deps import get_db_session
from aerial_photography import schemas
from aerial_photography import crud
from aerial_photography import models
from aerial_photography.utils.tile_operations import (
    convert_bytes_to_image,
    convert_image_to_bytes,
    clear_background,
    merge_tile)
import io

router = APIRouter()


@router.post("/add_user")
def add_user(
        *,
        db: Session = Depends(get_db_session),
        user_in: schemas.UserCreateSchema
):
    '''Функция для добавления пользователя в базу данных'''
    user = crud.user.create(db=db, obj_in=user_in)
    return {'message': 'Пользователь успешно добавлен в базу данных'}


@router.get("/get_user_by_login")
def get_user_by_login(
        *,
        db: Session = Depends(get_db_session),
        login: str
):
    '''Функция для получения плитки по координатам'''
    user = crud.user.get_user_by_login(db=db, login=login)
    if user is None:
        raise HTTPException(status_code=404, detail="A user with this username has not been found!")

    return user


@router.get("/get_user")
def get_user(
        *,
        db: Session = Depends(get_db_session),
        id: int
):
    '''Функция для получения плитки по координатам'''
    user = crud.user.get(db=db, id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="A user with this username has not been found!")

    return user
