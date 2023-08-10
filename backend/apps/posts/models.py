from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel

from apps.users.models import UserModel as User

from .choices.region_choices import RegionChoices
from .managers import PostManager

UserModel: User = get_user_model()


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
