import pytest


@pytest.mark.django_db
def test_ad_create(client, test_user):
    request_data = {
        "slug": "test_ad",
        "name": "test name",
        "author": "test_user_name test_user_surname",
        "author_id": 1,
        "price": 777,
        "description": "first test advertisement",
        "is_published": False,
    }


    expected_response = {
        "id": 1,
        "slug": request_data.get('slug'),
        "name": request_data.get('name'),
        "author": test_user.first_name,
        "author_id": test_user.id,
        "price": 777,
        "image": None,
        "category": None,
        "category_id": None,
        "description": "first test advertisement",
        "is_published": False
    }

    response = client.post('/ads/create/', request_data, format='json').json()
    assert expected_response == response
