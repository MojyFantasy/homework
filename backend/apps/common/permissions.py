from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUserOrCreator(BasePermission):
    """
    Allows access only to superuser or creator.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        if hasattr(obj, 'creator') and request.user is obj.creator:
            return True
        return False
