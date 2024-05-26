from letmecook.core.mongo_database import DB
from letmecook.user.models import UserDBModel
from letmecook.user.routes import collection_name

class TestDeleteFavorite:
    def test_delete_favorite(self, test_client, user_db_factory):
        recipe = 1234456
        user = user_db_factory
        test_client.get(f"/recipe/favorite/{recipe}/{user.id}")
        response = test_client.get(f"/recipe/delete-favorite/{recipe}/{user.id}")
        collection = DB[collection_name].find_one({"_id": user.id})
        db_user = UserDBModel.from_mongo(collection)
        assert response.status_code == 200
        assert len(db_user.recipies_like) == 0
