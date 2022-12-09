import pytest
from tests.factories import AdvertisementFactory
from ads.serializers import AdvertisementSerializer

@pytest.mark.django_db
def test_get_list_advertisement(client):
    advertisements = AdvertisementFactory.create_batch(5)
    response = client.get('/ads/')
    expected_response = {
        "total": 5,
        "num_pages": 1,
        "items": AdvertisementSerializer(advertisements, many=True).data
    }
    assert response.status_code == 200
    assert response.json() == expected_response
