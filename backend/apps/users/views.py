from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.dataclasses.user_dataclass import UserDataClass
from core.permission import IsAdminOrWriteOnlyPermission, IsSuperUser
from core.services.email_services import EmailService

from apps.users.models import UserModel as User

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
    permission_classes = (IsAdminOrWriteOnlyPermission,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


# class UserAddAvatarView(GenericAPIView):
#     serializer_class = AvatarSerializer
#
#     def put(self, *args, **kwargs):
#         serializer = self.get_serializer(self.request.user.profile, data=self.request.FILES)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)

class UserAddAvatarView(UpdateAPIView):
    """
     Add User avatar
    """
    serializer_class = AvatarSerializer
    http_method_names = ('put',)

    def get_object(self):
        return UserModel.objects.all_with_profile().get(pk=self.request.user.pk).profile

    # def perform_update(self, serializer):
    #     self.get_object().avatar.delete()
    #     super().perform_update(serializer)


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


class TestEmail(GenericAPIView):
    permission_classes = AllowAny,

    def get(self, *args, **kwargs):
        EmailService.test_email()
        return Response('ok')
