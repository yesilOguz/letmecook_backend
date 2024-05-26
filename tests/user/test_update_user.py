class TestUpdateUser:
    def test_update_user(self, test_client, user_update_factory):
        user = user_update_factory
        response = test_client.post("/user/update", json=user.to_json())
        assert response.status_code == 200
        assert user.username == response.json()["username"]

    def test_update_user_if_username_is_not_new(self, test_client, user_db_factory, user_update_with_params_factory):
        user = user_update_with_params_factory(user_db_factory.id, username=user_db_factory.username)
        response = test_client.post("/user/update", json=user.to_json())
        assert response.status_code == 400

    def test_update_user_if_password_is_not_new(self, test_client, user_db_factory, user_update_with_params_factory):
        user = user_update_with_params_factory(user_db_factory.id, password=user_db_factory.password)
        response = test_client.post("/user/update", json=user.to_json())
        assert response.status_code == 400

    def test_update_user_if_password_and_username_are_not_new(self, test_client, user_db_factory, user_update_with_params_factory):
        user = user_update_with_params_factory(user_db_factory.id, password=user_db_factory.password, username=user_db_factory.username)
        response = test_client.post("/user/update", json=user.to_json())
        assert response.status_code == 400

    def test_update_user_if_values_are_none(self, test_client, user_db_factory, user_update_with_params_factory):
        user = user_update_with_params_factory(id=user_db_factory.id, password=None, username=None, name=None)
        response = test_client.post("/user/update", json=user.to_json())
        assert response.status_code == 200
        assert response.json()["name"] == user_db_factory.name
        assert response.json()["username"] == user_db_factory.username
