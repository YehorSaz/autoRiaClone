from django.urls import path

from ..cars.views import CarCreateView
from .views import PostListView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('', PostListView.as_view()),
    path('/<int:pk>', PostRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/create_car', CarCreateView.as_view())
]
