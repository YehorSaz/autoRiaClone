from rest_framework import serializers

from .models import PhotoModel, PostModel, UserCarModel


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoModel
        fields = ('photo', 'car')
        read_only_fields = ('car',)
        extra_kwargs = {
            'photo': {
                'required': True
            }
        }


class UserCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCarModel
        fields = ('id', 'brand', 'model', 'price', 'currency', 'year', 'photos', 'created_at', 'updated_at')


class PostSerializer(serializers.ModelSerializer):
    car = UserCarSerializer()

    class Meta:
        model = PostModel
        fields = (
            'id', 'active_status', 'region', 'city', 'car', 'created_at', 'updated_at', 'user', 'views_count', 'update_count')
        read_only_fields = ('user', 'created_at', 'updated_at', 'active_status', 'views_count', 'update_count')

    def create(self, validated_data: dict):
        car = validated_data.pop('car')
        car = UserCarModel.objects.create(**car)
        post = PostModel.objects.create(car=car, **validated_data)
        return post
