from django.urls import path

from .views import AutoParkListCreateView, AutoParkCarListCreateView, AutoParkRetriveUpdateDestroyView

urlpatterns = [
    path('', AutoParkListCreateView.as_view()),
    path('/<int:pk>', AutoParkRetriveUpdateDestroyView.as_view()),
    path('/<int:pk>/cars', AutoParkCarListCreateView.as_view()),
]