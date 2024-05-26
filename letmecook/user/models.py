from letmecook.core.LetMeCookBaseModel import LetMeCookBaseModel, ObjectIdPydanticAnnotation
from typing import Optional, Annotated
from bson import ObjectId

class UserDBModel(LetMeCookBaseModel):
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]]
    name: str
    username: str
    password: str
    recipies_like: list[int] = []


class UserCreateResponse(LetMeCookBaseModel):
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]]
    name: str
    username: str
    recipies_like: list[int] = []

class UserLoginModel(LetMeCookBaseModel):
    username: str
    password: str

class UserUpdateModel(LetMeCookBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    name: Optional[str] = None
    username:  Optional[str] = None
    password: Optional[str] = None

class UserCreateModel(LetMeCookBaseModel):
    name: str
    username: str
    password: str

class UserGetMeResponse(LetMeCookBaseModel):
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]]
    name: str
    username: str
    recipies_like: list[int] = []

class UserGetUserResponse(LetMeCookBaseModel):
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]]
    name: str
    username: str
    recipies_like: list[int] = []
