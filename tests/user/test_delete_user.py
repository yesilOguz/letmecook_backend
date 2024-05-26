from bson import ObjectId
from letmecook.core.mongo_database import DB
from letmecook.user.routes import collection_name


class TestDeleteUser:
    def test_delete_user(self, test_client, user_db_factory):
        user = user_db_factory
        count = DB[collection_name].count_documents({})
        assert count == 1
        response = test_client.get(f"/user/delete/{user.id}")
        count = DB[collection_name].count_documents({})
        assert response.status_code == 200
        assert count == 0

    def test_delete_user_if_not_exist(self, test_client):
        user = ObjectId()
        response = test_client.get(f"/user/delete/{user}")
        assert response.status_code == 200

    def test_delete_user_if_user_id_invalid(self, test_client):
        user = "123456789"
        response = test_client.get(f"/user/delete/{user}")
        assert response.status_code == 400
