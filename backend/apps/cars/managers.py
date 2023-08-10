from django.db import models


class CarQuerySet(models.QuerySet):
    def get_car_by_post_id(self, pk):
        return self.filter(post_id=pk)


class CarManager(models.Manager):
    def get_queryset(self):
        return CarQuerySet(self.model)

    def get_car_by_post_id(self, pk):
        return self.get_queryset().get_car_by_post_id(pk)
