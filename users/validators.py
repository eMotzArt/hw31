from datetime import date, timedelta
from rest_framework import serializers

def OlderOrEqualNine(value: date):
    # if date.today() - value
    age = (date.today() - value) // timedelta(days=365.2425)
    if age < 9:
        raise serializers.ValidationError('EULA consider users older than 9 years')

def NotFromRambler(value: str):
    restricted_domain = [
        'rambler.ru'
    ]
    if value.split('@')[1] in restricted_domain:
        raise serializers.ValidationError('Your email domain is not allowed')
