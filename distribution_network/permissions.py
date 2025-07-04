# permissions.py
from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешает доступ только активным сотрудникам с is_staff=True
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_active