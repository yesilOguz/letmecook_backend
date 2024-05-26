import random

from bson import ObjectId

from letmecook.core.mongo_database import DB
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name


class TestGetFavorite:
    def test_get_favorite(self, test_client, user_db_factory, favorite_recipe_db_factory):
        user = user_db_factory
        favorite_recipe_db_factory(user_id=user.id)
        response = test_client.get(f"/recipe/get-favorite/{user.id}")
        collection = DB[collection_name].find_one({"_id": user.id})
        db_user = UserDBModel.from_mongo(collection)
        assert response.status_code == 200
        assert len(db_user.recipies_like) == 1

    def test_get_favorite_if_there_are_more_than_one_favorite(self, test_client,
                                                              user_db_factory, favorite_recipe_db_factory):
        count_of_recipe = random.randint(2, 100)
        user = user_db_factory
        favorite_recipe_db_factory(user_id=user.id, count=count_of_recipe)
        response = test_client.get(f"/recipe/get-favorite/{user.id}")
        collection = DB[collection_name].find_one({"_id": user.id})
        db_user = UserDBModel.from_mongo(collection)
        assert response.status_code == 200
        assert len(db_user.recipies_like) == count_of_recipe

    def test_get_favorite_if_user_id_is_wrong(self, test_client):
        user_id = ObjectId()
        response = test_client.get(f"/recipe/get-favorite/{user_id}")
        assert response.status_code == 400

    def test_get_favorite_if_user_id_is_invalid(self, test_client):
        user_id = "wrong_id"
        response = test_client.get(f"/recipe/get-favorite/{user_id}")
        assert response.status_code == 400

