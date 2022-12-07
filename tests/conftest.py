pytest_plugins = 'tests.fixtures'

from pytest_factoryboy import register

from tests.factories import AdvertisementFactory, UserFactory

register(AdvertisementFactory)
register(UserFactory)