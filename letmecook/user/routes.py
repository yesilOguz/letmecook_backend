from bson import ObjectId
from fastapi import APIRouter, Body, status, HTTPException
from letmecook.core.mongo_database import DB
from letmecook.recipe.validator import validate_object_id
from letmecook.user.models import UserDBModel, UserCreateResponse, UserLoginModel, UserUpdateModel, UserCreateModel, \
    UserGetMeResponse, UserGetUserResponse

collection_name = "user"
router = APIRouter()


@router.post("/create", status_code=status.HTTP_200_OK, response_model=UserCreateResponse)
def create_user(user: UserCreateModel = Body(...)):
    if user.username.strip() == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Kullanıcı adı boş bırakılamaz!")

    if len(user.username) <= 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Kullanıcı adı 6 karakterden kısa olamaz.")

    result = DB[collection_name].find_one({"username": user.username})

    if result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bu kullanıcı adı alınmış")

    if user.password.strip() == "":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Şifre boş bırakılamaz!")

    inserted = DB[collection_name].insert_one(user.to_mongo())

    result = DB[collection_name].find_one({"_id": inserted.inserted_id})
    user_response = UserCreateResponse.from_mongo(result)

    return user_response


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserCreateResponse)
def login_user(user: UserLoginModel = Body(...)):
    result = DB[collection_name].find_one({"username": user.username, "password": user.password})

    if result:
        return UserCreateResponse.from_mongo(result)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Kullanıcı Adı ya da Şifre Hatalı")


@router.post("/update", status_code=status.HTTP_200_OK, response_model=UserCreateResponse)
def update_user(user: UserUpdateModel = Body(...)):
    result = DB[collection_name].find_one({"_id": user.id})
    result = UserDBModel.from_mongo(result)

    if result:
        check_username = DB[collection_name].find_one({"username": user.username})
        check_username = UserDBModel.from_mongo(check_username)

        if check_username and check_username.username != result.username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bu kullanıcı adı alınmış")

        if check_username and check_username.username == result.username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Eski kullanıcı adı yeni kullanıcı adıyla aynı olamaz.")

        if user.password and result.password == user.password:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Eski şifre yeni şifreyle aynı olamaz.")

        DB[collection_name].find_one_and_update(filter={"_id": user.id},
                                                update={"$set": user.to_mongo(exclude_none=True)})

        updated = DB[collection_name].find_one({"_id": user.id})
        updated = UserCreateResponse.from_mongo(updated)

        return updated


@router.get("/delete/{user_id}", status_code=status.HTTP_200_OK, response_model=bool)
@validate_object_id('user_id')
def delete_user(user_id):
    DB[collection_name].find_one_and_delete({"_id": ObjectId(user_id)})

    return True


@router.get("/get-me/{user_id}", status_code=status.HTTP_200_OK, response_model=UserGetMeResponse)
@validate_object_id('user_id')
def get_me(user_id):
    result = DB[collection_name].find_one({"_id": ObjectId(user_id)})
    result = UserGetMeResponse.from_mongo(result)

    if result is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Kullanıcıyı bulamadık")

    return result


@router.get("/get-user/{user_name}", status_code=status.HTTP_200_OK, response_model=UserGetUserResponse)
def get_user(user_name):
    result = DB[collection_name].find_one({"username": user_name})
    result = UserGetUserResponse.from_mongo(result)

    if result is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Kullanıcıyı bulamadık.')

    return result
