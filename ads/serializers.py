from rest_framework import serializers

from ads.models import Location, Category, Advertisement
from ads.validators import IsPublishedMustBeFalse


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name']

class AdvertisementSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='first_name')
    author_id = serializers.IntegerField()
    image = serializers.ImageField(read_only=True)
    slug = serializers.CharField(allow_null=True)
    # is_published = serializers.BooleanField(validators=[IsPublishedMustBeFalse])
    class Meta:
        model = Advertisement
        fields = ['id', 'slug', 'name', 'price', 'description', 'image', 'is_published', 'author', 'author_id', 'category', 'category_id']