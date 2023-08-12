from datetime import datetime

from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_image_service import upload_image

from apps.cars.managers import CarManager
from apps.posts.choices.brand_choices import BrandChoices
from apps.posts.choices.currencies_choices import CurrenciesChoices
from apps.posts.models import PostModel


class ImageModel(BaseModel):
    class Meta:
        db_table = 'images'

    image = models.ImageField(upload_to=upload_image, blank=True)


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ('id',)

    brand = models.CharField(max_length=25, choices=BrandChoices.choices, validators=(
        V.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg),
    ))
    model = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(validators=(
        V.MinValueValidator(0),
        V.MaxValueValidator(100000000)
    ))
    currency = models.CharField(max_length=3, choices=CurrenciesChoices.choices)
    year = models.IntegerField(validators=(
        V.MinValueValidator(1935),
        V.MaxValueValidator(datetime.now().year)
    ))
    # post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='car')
    images = models.OneToOneField(ImageModel, on_delete=models.CASCADE, related_name='car', null=True)
    objects = models.Manager()
    my_objects = CarManager()
