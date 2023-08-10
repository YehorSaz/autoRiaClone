from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from core.services.email_services import EmailService

from apps.posts.serializers import PostSerializer
from apps.users.models import AvatarModel
from apps.users.models import UserModel as User

from .models import ProfileModel

UserModel: User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'phone', 'avatars')


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarModel
        fields = ('avatar',)
        extra_kwargs = {
            'avatar': {
                'required': True
            }
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = (
            'id', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'account_status', 'last_login',
            'created_at',
            'updated_at', 'profile', 'posts'
        )
        read_only_fields = (
            'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at',
            'updated_at', 'account_status'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        EmailService.register_email(user)
        return user
