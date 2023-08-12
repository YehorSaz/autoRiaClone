from rest_framework import serializers

from apps.currencies.models import CurrenciesModel


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrenciesModel
        fields = ('name', 'base_ccy', 'buy', 'sale')

    def create(self, validated_data: dict):
        course = CurrenciesModel.objects.create(**validated_data)
        return course
