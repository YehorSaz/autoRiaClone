from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permission.post_permissions import IsOwnerOrReadOnly
from core.services.censor_service.cesor_service import censor

from apps.users.models import UserModel as User

from .models import PostModel
from .serializers import PostSerializer

UserModel: User = get_user_model()


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class PostListView(ListAPIView):
    """
    Get all Posts
    """
    serializer_class = PostSerializer
    queryset = PostModel.objects.filter(active_status=True)
    permission_classes = (AllowAny,)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Get Post by id
    put:
        Full update Post by id
    patch:
        Partial update Post by id
    delete:
        Delete Post by id
    """
    serializer_class = PostSerializer
    queryset = PostModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return AllowAny(),
        elif self.request.method == 'DELETE':
            return IsAdminUser(),
        return IsOwnerOrReadOnly(),

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.update_count >= 3:
            return Response('only 3 times', status.HTTP_403_FORBIDDEN)
        post.update_count += 1
        post.save()
        censor_count = censor(self.request.data['city'])
        if censor_count <= 0:
            post.active_status = True
            post.save()
        else:
            post.active_status = False
            post.save()
            return Response('Знайдено підозрілу лексику, відредагуйте оголошення, оголошення не активне',
                            status.HTTP_201_CREATED)

        return super().patch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        post = self.get_object()
        post.views_count += 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)
