import pytest


@pytest.mark.django_db
def test_selection_create(client, test_user, test_user_token):
    request_data = {
        "slug": "test_seleciton",
        "name": "tester selection",
        "items": []
    }


    expected_response = {
        "id": 1,
        "name": request_data.get('name'),
        "items": []
    }

    x = client.post(
        '/user/token/',
        {"username": "test_username", "password": "test_password"},
        format="json"
    ).json().get('access')

    response = client.post('/selection/create/', request_data, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + x).json()
    assert expected_response == response
