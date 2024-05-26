class TestGetRandom:
    def test_get_random(self, test_client):
        type_of_food = ["vegetarian", "vegan", "gluten free", "dairy free", "low fodmap",
                        "french", "chinese", "italian", "mexican", "japanese"]

        response = test_client.get('/recipe/get-random')

        assert response.status_code == 200

        for random_food in type_of_food:
            assert len(response.json()[random_food]) > 0
