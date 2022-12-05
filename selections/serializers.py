from rest_framework import serializers
from selections.models import Collection
from ads.models import Advertisement
from users.models import User


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class CollectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"

class CollectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement,
        slug_field='id',
    )
    class Meta:
        model = Collection
        fields = ['id', 'name', 'items']

    def is_valid(self, *, raise_exception=False):
        self._ads = self.initial_data.pop('items')
        self.owner = self.context.get('request').user
        self.owner_id = self.context.get('request').user.id
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data['owner_id'] = self.owner_id
        collection = super().create(validated_data=validated_data)
        for ad in self._ads:
            try:
                finded_ad = Advertisement.objects.get(id=ad)
            except Advertisement.DoesNotExist:
                continue
            collection.items.add(finded_ad)
        collection.save()
        return collection

class CollectionUpdateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement,
        slug_field='id',
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field='first_name')

    class Meta:
        model = Collection
        fields = ['id', 'slug', 'name', 'items', 'owner', 'owner_id']

    def is_valid(self, *, raise_exception=False):
        self._ads = self.initial_data.pop('items')
        self.owner = self.context.get('request').user
        self.owner_id = self.context.get('request').user.id
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        collection = super().save(**kwargs)
        if not self._ads:
            return collection

        collection.items.clear()
        for ad in self._ads:
            try:
                finded_ad = Advertisement.objects.get(id=ad)
            except Advertisement.DoesNotExist:
                continue
            collection.items.add(finded_ad)
        collection.save()
        return collection


class CollectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id']
