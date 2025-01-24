from rest_framework.permissions import BasePermission

class IsEmployeeUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.user_type == 'employee'
    
class IsOwnerUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.user_type == 'owner'
