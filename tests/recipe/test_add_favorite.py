from bson import ObjectId

from letmecook.core.mongo_database import DB
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name


class TestAddFavorite:
    def test_add_favorite(self, test_client, user_db_factory):
        recipe = 150235
        user = user_db_factory
        response = test_client.get(f"/recipe/favorite/{recipe}/{user.id}")
        collection = DB[collection_name].find_one({"_id": user.id})
        db_user = UserDBModel.from_mongo(collection)
        assert response.status_code == 200
        assert response.json() is True
        assert len(db_user.recipies_like) == 1
        assert db_user.recipies_like[0] == recipe

    def test_add_favorite_if_recipe_is_alredy_favorited(self, test_client, user_db_factory):
        recipe = 150235
        user = user_db_factory
        test_client.get(f"/recipe/favorite/{recipe}/{user.id}")
        response = test_client.get(f"/recipe/favorite/{recipe}/{user.id}")
        collection = DB[collection_name].find_one({"_id": user.id})
        db_user = UserDBModel.from_mongo(collection)
        assert response.status_code == 400
        assert len(db_user.recipies_like) == 1
        assert db_user.recipies_like[0] == recipe

    def test_add_favorite_if_user_is_not_exist(self, test_client):
        recipe = 1234567
        user = ObjectId()
        response = test_client.get(f"/recipe/favorite/{recipe}/{user}")
        assert response.status_code == 400


