from django.urls import path

from .views import AutoParkCarListCreateView, AutoParkListCreateView, AutoParkRetriveUpdateDestroyView

urlpatterns = [
    path('', AutoParkListCreateView.as_view(), name='auto_parks_list_create'),
    path('/<int:pk>', AutoParkRetriveUpdateDestroyView.as_view(), name='auto_parks_retrive_update_destroy'),
    path('/<int:pk>/cars', AutoParkCarListCreateView.as_view()),
]