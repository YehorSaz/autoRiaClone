from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth.views import (
    ActivateUserView,
    AuthLoginView,
    AuthTokenView,
    MeView,
    NewUserPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    path('', AuthLoginView.as_view(), name='auth_login'),
    path('/recovery_pass', ResetPasswordView.as_view()),
    path('/recovery_pass/<str:token>', NewUserPasswordView.as_view()),
    path('/activate/<str:token>', ActivateUserView.as_view()),
    path('/refresh', TokenRefreshView.as_view()),
    path('/me', MeView.as_view()),
    path('/socket_token', AuthTokenView.as_view())
]
