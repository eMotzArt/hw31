import factory.django

from ads.models import Advertisement
from users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    slug = 'test_user'
    first_name = "test_user_name"
    last_name = "test_user_surname"
    username = factory.Faker('name')
    password = "test_password"
    role = "admin"
    email = factory.Faker('email')
    age = 31
    birth_date = "1991-01-01"
    

class AdvertisementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advertisement

    slug = "test_ad"
    name = "test name"
    author = factory.SubFactory(UserFactory)
    price = 777
    description = "first test advertisement"
    is_published = False
