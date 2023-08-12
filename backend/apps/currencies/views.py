from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from core.services.email_services import get_courses

from apps.currencies.models import CurrenciesModel
from apps.currencies.serializers import CurrenciesSerializer


class CurrenciesCreateView(ListCreateAPIView):
    queryset = CurrenciesModel.objects.all()
    permission_classes = (IsAdminUser,)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        data = self.request.data
        serializer = CurrenciesSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        exists = CurrenciesModel.objects.filter(pk=pk).exists()
        if not exists:
            if CurrenciesModel.objects.count() >= 2:
                return Response('Not allowed', status.HTTP_403_FORBIDDEN)
            serializer.save(id=pk)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            get_courses()
            return Response('Automatically set from Privatbank', status.HTTP_201_CREATED)


class CurrenciesListView(ListAPIView):
    serializer_class = CurrenciesSerializer
    queryset = CurrenciesModel.objects.all()
    permission_classes = (AllowAny,)
