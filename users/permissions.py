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
        if obj.owner == request.user:
            return True
        return False