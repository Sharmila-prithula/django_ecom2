from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.user==obj:
        #     return True
        # else:
        #     return False
        #return self.check_object_permission(request.user, obj)
        if request.method in permissions.SAFE_METHODS:
            return False

        # Instance must have an attribute named `owner`.
        return obj.vendor_owner == request.user