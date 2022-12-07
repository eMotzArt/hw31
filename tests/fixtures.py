import pytest


@pytest.fixture
@pytest.mark.django_db
def test_user(django_user_model):
    user_data = {
        "slug": 'test_user',
        "first_name": "test_user_name",
        "last_name": "test_user_surname",
        "username": "test_username",
        "password": "test_password",
        "role": "admin",
        "email": "test@email.me",
        "age": 31,
        "birth_date": "1991-01-01"
    }
    user = django_user_model.objects.create(**user_data)
    user.set_password(user.password)
    user.save()

    return user


@pytest.fixture
@pytest.mark.django_db
def test_user_token(client, test_user, django_user_model):
    response = client.post(
        '/user/token/',
        {"username": "test_username", "password": "test_password"},
        format="json"
    )

    return response.data["access"]