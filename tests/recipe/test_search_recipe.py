class TestSearchRecipe:
    def test_search_recipe(self, test_client, recipe_name_factory):
        recipe = recipe_name_factory
        response = test_client.get(f"/recipe/search-recipe/{recipe}")
        assert response.status_code == 200
        assert len(response.json()["results"]) > 0

    def test_search_recipe_if_value_is_wrong(self, test_client):
        recipe = "wrong_ingredient_name"
        response = test_client.get(f"/recipe/search-recipe/{recipe}")
        assert response.status_code == 200
        assert len(response.json()["results"]) == 0

    def test_search_recipe_if_recipe_name_is_none(self, test_client):
        recipe = " "
        response = test_client.get(f"/recipe/search-recipe/{recipe}")
        assert response.status_code == 400



