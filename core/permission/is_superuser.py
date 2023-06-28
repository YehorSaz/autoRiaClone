from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):

    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and request.user.is_superuser)