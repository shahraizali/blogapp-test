from rest_framework import permissions


class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and hasattr(request.user, "writer_user")
            and request.user.writer_user.is_editor
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.edited_by.user if hasattr(obj.edited_by, "user") else 0
        )
