from bson import ObjectId

class TestUserGetMe:
    def test_get_me(self, test_client, user_db_factory):
        user = user_db_factory
        response = test_client.get(f"/user/get-me/{user.id}")
        assert user.username == response.json()["username"]
        assert response.status_code == 200

    def test_get_me_if_not_exist(self, test_client):
        user = ObjectId()
        response = test_client.get(f"/user/get-me/{user}")
        assert response.status_code == 400

    def test_get_me_if_user_id_is_not_valid(self, test_client):
        user = "invalid_id"
        response = test_client.get(f"/user/get-me/{user}")
        assert response.status_code == 400
