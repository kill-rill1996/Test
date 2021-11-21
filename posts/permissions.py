from rest_framework import permissions


class IsPostOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user
