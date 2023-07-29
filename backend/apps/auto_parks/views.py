from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer

from .models import AutoParkModel
from .serializers import AutoParkSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class AutoParkListCreateView(ListCreateAPIView):
    """
        get:
            Get all Auto parks
        post:
            Create Auto park
    """
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all_with_cars()

    def get_permissions(self):
        if self.request.method == 'GET':
            return AllowAny(),

        return IsAdminUser(),
    # permission_classes = (IsAdminUser,)


class AutoParkRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
        get:
            Get Auto park by id
        put:
            Update Auto park by id
        patch:
            Partial update Auto park by id
        delete:
            Delete Auto park by id
    """
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()


class AutoParkCarListCreateView(GenericAPIView):
    """
        get:
            Get cars by auto_park id
        post:
            Create Car
    """
    queryset = AutoParkModel.objects.all()
    serializer_class = CarSerializer

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not AutoParkModel.objects.filter(pk=pk).exists():
            raise Http404()

        cars = CarModel.objects.filter(auto_park_id=pk)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        exists = AutoParkModel.objects.filter(pk=pk).exists()
        if not exists:
            raise Http404()
        serializer.save(auto_park_id=pk)
        return Response(serializer.data, status.HTTP_201_CREATED)
