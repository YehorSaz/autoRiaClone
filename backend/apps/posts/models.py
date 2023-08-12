from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel

from apps.users.models import UserModel as User

from .choices.region_choices import RegionChoices
from .managers import PostManager

UserModel: User = get_user_model()


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


class PostModel(BaseModel):
    class Meta:
        db_table = 'posts'
        ordering = ('id',)

    views_count = models.IntegerField(default=0)
    active_status = models.BooleanField(default=True)

    region = models.CharField(max_length=19, choices=RegionChoices.choices)

    descriptions = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    objects = models.Manager()
    # my_objects = PostManager()
