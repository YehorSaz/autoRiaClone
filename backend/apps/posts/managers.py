from django.db import models


class PostQuerySet(models.QuerySet):
    def get_posts_by_user_id(self, pk):
        return self.filter(user_id=pk)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def get_posts_by_user_id(self, pk):
        return self.get_queryset().get_posts_by_user_id(pk)

    def all_with_cars(self):
        return self.prefetch_related('car')


class UserCarQuerySet(models.QuerySet):
    def get_car_by_post_id(self, pk):
        return self.filter(post_id=pk)


class UserCarManager(models.Manager):
    def get_queryset(self):
        return UserCarQuerySet(self.model)

    def get_car_by_post_id(self, pk):
        return self.get_queryset().get_car_by_post_id(pk)
