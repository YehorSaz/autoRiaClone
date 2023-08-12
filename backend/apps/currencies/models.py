from django.db import models

from core.models import BaseModel


class CurrenciesModel(BaseModel):
    class Meta:
        db_table = 'currencies'
        ordering = ('id',)

    name = models.CharField(max_length=3)
    base_ccy = models.CharField(max_length=3)
    buy = models.FloatField()
    sale = models.FloatField()
