import pytest
from ads.serializers import AdvertisementSerializer

@pytest.mark.django_db
def test_get_detail_view(client, advertisement, test_user_token):

    response = client.get(f'/ads/{advertisement.pk}', HTTP_AUTHORIZATION="Bearer "+test_user_token).json()
    assert response == AdvertisementSerializer(advertisement).data