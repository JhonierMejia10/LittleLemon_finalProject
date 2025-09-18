from rest_framework import permissions

class IsGestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Gestor').exists()
