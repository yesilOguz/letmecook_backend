class TestGetFavoriteByUsername:
    def test_get_favorite_by_username(self, test_client, user_db_factory, favorite_recipe_db_factory):
        user = user_db_factory
        favorite_recipe_db_factory(user_id=user.id)

        response = test_client.get(f'/recipe/get-favorite-by-username/{user.username}')

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert 0 in response.json()

    def test_get_favorite_by_username_if_there_are_more_than_one_favorited(self, test_client,
                                                                           user_db_factory, favorite_recipe_db_factory):
        user = user_db_factory
        favorite_recipe_db_factory(user_id=user.id, count=5)

        response = test_client.get(f'/recipe/get-favorite-by-username/{user.username}')

        assert response.status_code == 200
        assert len(response.json()) == 5
        assert 4 in response.json()

    def test_get_favorite_by_username_if_username_not_exist(self, test_client):
        username = "wrong_username"

        response = test_client.get(f'/recipe/get-favorite-by-username/{username}')

        assert response.status_code == 404
