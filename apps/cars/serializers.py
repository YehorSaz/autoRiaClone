from rest_framework import serializers

from .models import CarModel


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'body', 'price', 'year', 'created_at', 'updated_at')

    # def validate(self, attrs):
    #     price = attrs.get('price')
    #     year = attrs.get('year')
    #     if price == year:
    #         raise serializers.ValidationError({'detail': 'price == year'})
    #     return super().validate(attrs)

    # def validate_brand(self, brand):
    #     if brand == 'Ssss':
    #         raise serializers.ValidationError({'detail': "brand not valid"})




