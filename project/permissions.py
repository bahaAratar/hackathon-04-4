from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """
    Дает разрешение использовать только пользователем у кого статус Клиент
    """

    def has_permission(self, request, view):
        return request.user.client
