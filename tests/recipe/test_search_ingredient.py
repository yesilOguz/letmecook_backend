class TestSearchIngredient:
    def test_search_ingredient(self,test_client, ingredients_name_factory):
        ingredient = ingredients_name_factory
        response = test_client.get(f"/recipe/search/{ingredient}")
        assert len(response.json()) > 0
        assert response.status_code == 200

    def test_search_ingredient_if_value_is_wrong(self, test_client):
        ingredient = "wrong_ingredient"
        response = test_client.get(f"/recipe/search/{ingredient}")
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_search_ingredient_if_value_is_none(self, test_client):
        ingredient = " "
        response = test_client.get(f"/recipe/search/{ingredient}")
        assert response.status_code == 400




