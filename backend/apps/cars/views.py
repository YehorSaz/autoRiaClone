from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permission.post_permissions import IsOwnerOrReadOnly

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer, ImageSerializer
from apps.posts.models import PostModel


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(ListAPIView):
    """
    Get all Cars
    """
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAdminUser,)


class CarCreateView(GenericAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        exists = PostModel.objects.filter(pk=pk).exists()
        if not exists:
            raise Http404()
        serializer.save(post_id=pk)
        return Response(serializer.data, status.HTTP_201_CREATED)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Get Car by id
    put:
        Full update Car by id
    patch:
        Partial update Car by id
    delete:
        Delete Car by id
    """
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()


class AddImageView(UpdateAPIView):
    """
        Add post image
    """
    serializer_class = ImageSerializer
    http_method_names = ('put',)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        return PostModel.objects.all_with_cars().get(pk=self.request.user.pk).posts
