def test_main_app(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {'LetMeCook!': 'v1.0'}
