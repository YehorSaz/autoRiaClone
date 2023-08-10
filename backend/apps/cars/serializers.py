from rest_framework import serializers

from apps.cars.models import CarModel, ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('image', 'car')
        read_only_fields = ('car',)
        extra_kwargs = {
            'image': {
                'required': True
            }
        }


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'model', 'price', 'year', 'images', 'created_at', 'updated_at', 'post')
        read_only_fields = ('post',)
