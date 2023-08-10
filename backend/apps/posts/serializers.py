from rest_framework import serializers

from ..cars.serializers import CarSerializer
from .models import PostModel


class PostSerializer(serializers.ModelSerializer):
    car = CarSerializer(many=True, read_only=True)

    class Meta:
        model = PostModel
        fields = (
            'id', 'active_status', 'region', 'car', 'created_at', 'updated_at',
            'descriptions', 'user', 'views_count')
        read_only_fields = ('user', 'created_at', 'updated_at', 'active_status', 'views_count')
