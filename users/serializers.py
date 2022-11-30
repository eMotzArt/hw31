from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True, slug_field='name')
    total_published_ads = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'slug', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'location', 'total_published_ads']

    def get_total_published_ads(self, user):
        return user.advertisement_set.filter(is_published=True).count()


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(user.password)
        user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    location = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'slug', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

class UserDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id']
