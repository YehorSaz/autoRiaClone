from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_avatar_service import upload_avatar

from .managers import UserManager


class AvatarModel(BaseModel):
    class Meta:
        db_table = 'avatars'

    avatar = models.ImageField(upload_to=upload_avatar, blank=True)


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'

    name = models.CharField(max_length=50, validators=[
        V.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])
    surname = models.CharField(max_length=50, validators=[
        V.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])
    age = models.IntegerField(validators=[
        V.MinValueValidator(18),
        V.MaxValueValidator(100)
    ])
    phone = models.IntegerField()
    avatars = models.OneToOneField(AvatarModel, on_delete=models.CASCADE, related_name='profile', null=True)


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[
        V.RegexValidator(RegExEnum.PASSWORD.pattern, RegExEnum.PASSWORD.msg)
    ])
    account_status = models.CharField(max_length=7, default='base')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user', null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
