def test_root(client):
    assert True
    response = client.get('/').json()
    expected_response = {'status': 'ok'}
    assert response == expected_response
