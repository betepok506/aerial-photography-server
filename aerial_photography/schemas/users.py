from typing import Union, Iterable, List, Tuple, ByteString
from pydantic import BaseModel
from sqlalchemy import LargeBinary


class User(BaseModel):
    '''Схема модели в БД'''
    login: str
    username: str
    password: str


class UserCreate(User):
    pass


class UserUpdate(User):
    pass


class UserSchema(BaseModel):
    '''Схема'''
    login: str
    username: str
    password: str



class UserCreateSchema(UserSchema):
    pass


class UserUpdateSchema(UserSchema):
    pass


class UserDeleteSchema(BaseModel):
    ids: int

