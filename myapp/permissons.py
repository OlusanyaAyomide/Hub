from rest_framework import permissions

class PublicQuestionPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_anonymous:
                return False
            return True

class AdminPermision(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

class AdminOrGetpermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_admin:
                return True
            return False