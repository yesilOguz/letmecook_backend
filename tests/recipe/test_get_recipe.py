class TestGetRecipe:
    def test_get_recipe(self, test_client, recipe_id_factory):
        recipe_id = recipe_id_factory

        response = test_client.get(f'/recipe/get-recipe/{recipe_id}')

        assert response.status_code == 200
        assert len(response.json()['similar']) > 0

    def test_get_recipe_if_recipe_doesnt_exist(self, test_client):
        recipe_id = "wrong_id"

        response = test_client.get(f'/recipe/get-recipe/{recipe_id}')

        assert response.status_code == 400

    def test_get_recipe_if_recipe_id_empty(self, test_client):
        recipe_id = " "

        response = test_client.get(f'/recipe/get-recipe/{recipe_id}')

        assert response.status_code == 400
