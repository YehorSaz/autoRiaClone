from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

from core.dataclasses.user_dataclass import UserDataClass
from core.services.email_services import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

from .serializers import EmailSerializer, PasswordSerializer

UserModel: User = get_user_model()


class MeView(RetrieveAPIView):
    """
        Information of current User
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class AuthLoginView(TokenObtainPairView):
    """
        Takes a set of user credentials and returns an access and refresh JSON web
        token pair to prove the authentication of those credentials.
        """
    permission_classes = AllowAny,


class ActivateUserView(GenericAPIView):
    """
        Takes token
        Activate User by token
        set User is_active = True
    """
    permission_classes = AllowAny,
    serializer_class = UserSerializer

    @staticmethod
    @swagger_auto_schema(request_body=no_body)
    def post(self, *args, **kwargs):
        token = kwargs['token']
        user: User = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class ResetPasswordView(GenericAPIView):
    """
        Takes e-mail
        Sending to e-mail a link to change the password
        and returns message "email has been sent"
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.change_password(user)
        return Response('email has been sent', status.HTTP_200_OK)
    # queryset = User.objects.all()
    # filter_class = UserFilter
    #
    # def post(self, *args, **kwargs):
    #     email = self.request.POST.get('email')
    #     if not User.objects.filter(email=email).exists():
    #         raise Http404()
    #     user: UserDataClass = User.objects.get(email=email)
    #     serializer = UserSerializer(user)
    #     EmailService.email_change(user)
    #     return Response('email has been sent', status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class NewUserPasswordView(GenericAPIView):
    """
        Takes token (in path)
        Change password and
        Returns message "the password has been changed"
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user: User = JWTService.validate_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response('the password has been changed', status.HTTP_200_OK)
        # password = self.request.POST.get('password')
        # token = kwargs['token']
        # user: User = JWTService.validate_token(token, ActivateToken)
        # user.set_password(password)
        # user.is_active = True
        # user.save()
        # serializer = UserSerializer(user)
        # return Response('the password has been changed', status.HTTP_200_OK)



