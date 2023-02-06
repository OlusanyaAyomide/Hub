from rest_framework import permissions

class PublicQuestionPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return True
          