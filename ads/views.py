from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import json
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.permissions import IsAuthor, IsModerator, IsAdmin
from project import settings
from ads.models import Category, Advertisement, Location
from ads.serializers import LocationSerializer, AdvertisementSerializer, CategorySerializer
from users.models import User

def index(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = {
            'items': CategorySerializer(page_obj, many=True).data,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }
        return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail_view(request, *args, **kwargs):
    try:
        category = Category.objects.get(id=kwargs.get('pk'))
    except Http404:
        return JsonResponse({'error': 'Not found'}, status=404)

    return JsonResponse(category.get_dict(), safe=False)


    try:
        super().get(request, *args, **kwargs)
    except Http404:
        return JsonResponse({'error': 'Not found'}, status=404)

    return JsonResponse(CategorySerializer(self.object).data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category.objects.create(name=category_data['name'])
        return JsonResponse(category.get_dict(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data['name']

        self.object.save()
        return JsonResponse(self.object.get_dict(), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)



@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementsListView(ListView):
    queryset = Advertisement.objects.all()
    model = Advertisement


    def get(self, request, *args, **kwargs):
        if category_id := request.GET.get('cat'):
            self.queryset = self.queryset.filter(category_id=category_id)
        if topic_text := request.GET.get('text'):
            self.queryset = self.queryset.filter(name__icontains=topic_text)
        if location := request.GET.get('location'):
            self.queryset = self.queryset.filter(author__location__name__icontains=location)
        if price_from := request.GET.get('price_from'):
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to := request.GET.get('price_to'):
            self.queryset = self.queryset.filter(price__lte=price_to)

        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('-price')


        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = {
            'items': AdvertisementSerializer(page_obj, many=True).data,
            'num_pages': paginator.num_pages,
            'total': paginator.count
        }
        return JsonResponse(response, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementsDetailView(RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]


    # def get(self, request, *args, **kwargs):
    #     try:
    #         super().get(request, *args, **kwargs)
    #     except Http404:
    #         return JsonResponse({'error': 'Not found'}, status=404)
    #     return JsonResponse(AdvertisementSerializer(self.object).data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementsCreateView(CreateView):
    model = Advertisement
    fields = ['name', 'author', 'price', 'description', 'category', 'is_published']
    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author_first_name, author_last_name = ad_data['author'].split()
        try:
            author = get_object_or_404(User, first_name=author_first_name, last_name=author_last_name)
        except Http404:
            return JsonResponse({'status': 'Author not found'}, status=404)

        category_data = ad_data['category']
        category, _ = Category.objects.get_or_create(name=category_data)

        ad = Advertisement.objects.create(name=ad_data['name'],
                                          author=author,
                                          price=ad_data['price'],
                                          description=ad_data['description'],
                                          category=category,
                                          is_published=ad_data['is_published']
                                          )
        return JsonResponse(ad.get_dict(), safe=False)

class AdvertisementsUpdateView(UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthor | IsAdmin | IsModerator]
    # fields = ['name', 'author', 'price', 'description', 'category', 'is_published']
    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     ad_data = json.loads(request.body)
    #
    #     author_first_name, author_last_name = ad_data['author'].split()
    #     try:
    #         author = get_object_or_404(User, first_name=author_first_name, last_name=author_last_name)
    #     except Http404:
    #         return JsonResponse({'status': 'Author not found'}, status=404)
    #
    #     category_data = ad_data['category']
    #     category, _ = Category.objects.get_or_create(name=category_data)
    #
    #
    #     self.object.name = ad_data['name']
    #     self.object.author = author
    #     self.object.price = ad_data['price']
    #     self.object.description = ad_data['description']
    #     self.object.category = category
    #     self.object.is_published = ad_data['is_published']
    #
    #     return JsonResponse(self.object.get_dict(), safe=False)

class AdvertisementsDeleteView(DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthor | IsAdmin | IsModerator]
    # success_url = "/"

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({'status': 'ok'}, status=200)


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
