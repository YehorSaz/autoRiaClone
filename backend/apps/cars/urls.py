from django.urls import path

from .views import AddImageView, CarListView, CarRetrieveUpdateDestroyView

urlpatterns = [
    path('', CarListView.as_view()),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
    path('/image', AddImageView.as_view())
]
