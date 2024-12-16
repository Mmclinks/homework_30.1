from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    """
    Разрешение для проверки, является ли пользователь модератором.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()



class IsOwnerOrReadOnly(BasePermission):
    """
    Права доступа, позволяющие редактировать и удалять только свои объекты.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user  # Проверяем, является ли пользователь владельцем
