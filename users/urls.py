from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import users.views

urlpatterns = [
    path('user/', users.views.UsersListView.as_view()),
    path('user/create/', users.views.UserCreateView.as_view()),
    path('user/<int:pk>', users.views.UserDetailView.as_view()),
    path('user/<int:pk>/update/', users.views.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', users.views.UserDeleteView.as_view()),
    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
