from django.urls import path

import selections.views

urlpatterns = [
    path('selection/', selections.views.CollectionListView.as_view()),
    path('selection/create/', selections.views.CollectionCreateView.as_view()),
    path('selection/<int:pk>/', selections.views.CollectionDetailView.as_view()),
    path('selection/<int:pk>/update/', selections.views.CollectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', selections.views.CollectionDeleteView.as_view()),
]
