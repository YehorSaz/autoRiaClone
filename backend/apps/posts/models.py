from datetime import datetime

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_image_service import upload_image

from apps.users.models import UserModel as User

from .choices.brand_choices import BrandChoices
from .choices.currencies_choices import CurrenciesChoices
from .choices.region_choices import RegionChoices
from .managers import PostManager, UserCarManager

UserModel: User = get_user_model()


class PhotoModel(BaseModel):
    class Meta:
        db_table = 'photos'

    photo = models.ImageField(upload_to=upload_image, blank=True)


class UserCarModel(BaseModel):
    class Meta:
        db_table = 'user_cars'
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

    photos = models.OneToOneField(PhotoModel, on_delete=models.CASCADE, related_name='car', null=True)
    objects = models.Manager()
    # my_objects = UserCarManager()


class PostModel(BaseModel):
    class Meta:
        db_table = 'posts'
        ordering = ('id',)

    views_count = models.IntegerField(default=0)
    update_count = models.IntegerField(default=0)
    active_status = models.BooleanField(default=False)

    region = models.CharField(max_length=19, choices=RegionChoices.choices)
    city = models.CharField(max_length=49, validators=[
        V.RegexValidator(RegExEnum.CITY.pattern, RegExEnum.CITY.msg)
    ])
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    car = models.OneToOneField(UserCarModel, on_delete=models.CASCADE, related_name='post', null=True)
    objects = models.Manager()
    my_objects = PostManager()
