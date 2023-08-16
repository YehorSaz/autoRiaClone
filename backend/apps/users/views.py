from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.dataclasses.user_dataclass import UserDataClass
from core.permission import IsSuperUser
from core.permission.post_permissions import IsOwnerOrReadOnly
from core.services.censor_service.cesor_service import censor

from apps.users.models import UserModel as User

from ..posts.models import PostModel
from ..posts.serializers import PostSerializer
from .filters import UserFilter
from .serializers import AvatarSerializer, UserSerializer

UserModel: User = get_user_model()


class UserListCreateView(ListCreateAPIView):
    """
        get:
            Get all Users
        post:
            Create User
    """

    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profile()
    filterset_class = UserFilter
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserAddAvatarView(UpdateAPIView):
    """
     Add User avatar
    """
    serializer_class = AvatarSerializer
    http_method_names = ('put',)

    def get_object(self):
        return UserModel.objects.all_with_profile().get(pk=self.request.user.pk).profile


class UserToAdminView(GenericAPIView):
    """
        Set User permission is_staff: True by id
    """
    permission_classes = IsSuperUser,
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user: UserDataClass = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    """
        Set User permission is_staff: False by id
    """
    permission_classes = IsSuperUser,
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    """
        Block User by id
    """
    permission_classes = IsAdminUser,
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    """
        Unblock User by id
    """
    permission_classes = IsAdminUser,
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockAdminUserView(BlockUserView):
    permission_classes = IsSuperUser

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UnBlockAdminUserView(UnBlockUserView):
    permission_classes = IsSuperUser

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserPostListCreateView(GenericAPIView):
    """
        get:
            Get posts by user id
        post:
            Create Post
    """
    queryset = UserModel.objects.all_with_profile()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return IsOwnerOrReadOnly(),
        return AllowAny(),

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not UserModel.objects.filter(pk=pk).exists():
            raise Http404()

        post = PostModel.objects.filter(user_id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pk = self.request.user.pk
        user: UserDataClass = self.request.user
        data = self.request.data
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        exists = UserModel.objects.filter(pk=pk).exists()
        if not exists:
            raise Http404()
        elif user.posts.count() >= 1 and user.account_status == 'base':
            return Response('Only 1 post for Base account', status.HTTP_403_FORBIDDEN)
        serializer.save(user_id=pk)
        censor_count = censor(data.get('city'))
        if censor_count <= 0:
            serializer.save(active_status=True)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response('Знайдено підозрілу лексику, відредагуйте оголошення, оголошення не активне',
                            status.HTTP_201_CREATED)
