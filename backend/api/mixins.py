from rest_framework import permissions
from .permissions import IsStaffEditorPermissions


class StaffEditorPermissionMixin:
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermissions]


class UserQuerysetMixin:
    user_field = "user"
    ALLOW_STAFF_VIEW = True

    def get_queryset(self, *args, **kwargs):
        lookup_data = {self.user_field: self.request.user}
        qs = super().get_queryset(*args, **kwargs)
        if self.ALLOW_STAFF_VIEW and self.request.user.is_staff:
            return qs
        return qs.filter(**lookup_data)
