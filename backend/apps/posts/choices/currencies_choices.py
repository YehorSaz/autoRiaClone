from django.db import models


class CurrenciesChoices(models.TextChoices):
    UAH = "UAH",
    USD = "USD",
    EUR = "EUR"
