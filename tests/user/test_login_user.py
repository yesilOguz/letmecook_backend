class TestLoginUser:
    def test_login_user(self, test_client, user_login_factory):
        user = user_login_factory
        response = test_client.post("/user/login", json=user.to_json())
        assert response.status_code == 200
        assert response.json()["username"] == user.username

    def test_login_user_if_password_is_wrong(self, test_client, user_login_factory):
        user = user_login_factory
        user.password = "wrong_password"
        response = test_client.post("/user/login", json=user.to_json())
        assert response.status_code == 401

    def test_login_user_if_username_is_wrong(self, test_client, user_login_factory):
        user = user_login_factory
        user.username = "wrong_username"
        response = test_client.post("/user/login", json=user.to_json())
        assert response.status_code == 401

    def test_login_user_if_password_and_username_are_wrong(self, test_client, user_login_factory):
        user = user_login_factory
        user.username = "wrong_username"
        user.password = "wrong_password"
        response = test_client.post("/user/login", json=user.to_json())
        assert response.status_code == 401


