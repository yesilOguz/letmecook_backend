class TestCreateUser:
    def test_create_user(self, test_client, user_create_factory):
        user = user_create_factory
        response = test_client.post("/user/create", json=user.to_json())
        assert response.status_code == 200
        assert response.json()["name"] == user.name

    def test_create_user_if_username_exist(self, test_client, user_create_factory):
        user = user_create_factory
        test_client.post("/user/create", json=user.to_json())
        response = test_client.post("/user/create", json=user.to_json())
        assert response.status_code == 400

    def test_create_user_if_username_is_null(self, test_client, user_create_factory):
        user = user_create_factory
        user.username = ""
        response = test_client.post("/user/create", json=user.to_json())
        assert response.status_code == 400

    def test_create_user_if_username_is_short(self, test_client,user_create_factory):
        user = user_create_factory
        user.username = "short"
        response = test_client.post("/user/create", json=user.to_json())
        assert response.status_code == 400

    def test_create_user_if_password_is_null(self, test_client, user_create_factory):
        user = user_create_factory
        user.password = ""
        response = test_client.post("/user/create", json=user.to_json())
        assert response.status_code == 400
