from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from selections.permissions import IsCollectionOwner
from selections.models import Collection
from selections.serializers import CollectionListSerializer, \
    CollectionDetailSerializer, \
    CollectionCreateSerializer, \
    CollectionUpdateSerializer, \
    CollectionDestroySerializer


class CollectionListView(ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionListSerializer

class CollectionDetailView(RetrieveAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionDetailSerializer

class CollectionCreateView(CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionCreateSerializer
    permission_classes = [IsAuthenticated]


class CollectionUpdateView(UpdateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionUpdateSerializer
    permission_classes = [IsCollectionOwner]


class CollectionDeleteView(DestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionDestroySerializer
    permission_classes = [IsCollectionOwner]
