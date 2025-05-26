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


@router.post("/add_tiles")
def add_tiles(
        *,
        db: Session = Depends(get_db_session),
        tiles_in: schemas.TilesCreateSchema
):
    '''Функция для добавления плиток в базу данных'''
    # added_tiles = []
    for tile_in in tiles_in.tiles:
        # Запрашиваем снимок с БД
        found_tile = crud.tiles.get_tiles_by_coordinates(db, x=tile_in.x, y=tile_in.y, z=tile_in.z)
        # Если снимок не найден в базе, добавляем
        if found_tile is None:
            clear_image = clear_background(convert_bytes_to_image(tile_in.image))
            bytes_img = convert_image_to_bytes(clear_image)

            added_tile = crud.tiles.create(db=db, db_obj=models.Tiles(x=tile_in.x,
                                                                      y=tile_in.y,
                                                                      z=tile_in.z,
                                                                      image=bytes_img))
            # added_tiles.append(added_tile)
        else:
            # Плитка была добавлена ранее, необходимо смержить
            merged_tile = merge_tile(found_tile, tile_in)
            added_tile = crud.tiles.create(db=db, db_obj=models.Tiles(x=merged_tile.x,
                                                                      y=merged_tile.y,
                                                                      z=merged_tile.z,
                                                                      image=merged_tile.image))
            # added_tiles.append(added_tile)

    # return 1


@router.get("/get_tiles_by_coordinates")
def get_tiles_by_coordinates(
        *,
        db: Session = Depends(get_db_session),
        z: int, x: int, y: int, type_obj: str
):
    print(type_obj)
    '''Функция для получения плитки по координатам'''
    tile = crud.tiles.get_tiles_by_coordinates(db, x=x, y=y, z=z)
    if tile is not None:
        base64_decoded = base64.decodebytes(tile.image)
        return Response(
            content=base64_decoded,
            media_type='image/png',
        )
    else:
        return Response(
            content=b'',
            media_type='image/png',
        )
