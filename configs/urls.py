from django.urls import path

from cars.views import CarListCreateView, CarRetriveUpdateDestroyView

urlpatterns = [
    path('cars', CarListCreateView.as_view()),
    path('cars/<int:pk>', CarRetriveUpdateDestroyView.as_view())
]
