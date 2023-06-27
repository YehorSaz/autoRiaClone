from django.urls import path

from .views import AutoParkCarListCreateView, AutoParkListCreateView, AutoParkRetriveUpdateDestroyView

urlpatterns = [
    path('', AutoParkListCreateView.as_view()),
    path('/<int:pk>', AutoParkRetriveUpdateDestroyView.as_view()),
    path('/<int:pk>/cars', AutoParkCarListCreateView.as_view()),
]