class TestGetUser:
    def test_get_user(self, test_client, user_db_factory):
        user = user_db_factory
        response = test_client.get(f"/user/get-user/{user.username}")
        assert user.username == response.json()["username"]
        assert response.status_code == 200

    def test_get_user_if_not_exist(self, test_client):
        user = "invalid_name"
        response = test_client.get(f"/user/get-user/{user}")
        assert response.status_code == 400


