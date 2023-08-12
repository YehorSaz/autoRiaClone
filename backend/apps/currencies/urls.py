from django.urls import path

from apps.currencies.views import CurrenciesCreateView, CurrenciesListView

urlpatterns =[
    path('', CurrenciesListView.as_view()),
    path('/<int:pk>', CurrenciesCreateView.as_view())
]
