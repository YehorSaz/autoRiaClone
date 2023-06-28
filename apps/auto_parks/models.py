from django.db import models

from core.models import BaseModel

from .managers import AutoParkManager


class AutoParkModel(BaseModel):
    class Meta:
        db_table = 'auto_parks'
        ordering = ('id',)

    name = models.CharField(max_length=25)
    objects = AutoParkManager()