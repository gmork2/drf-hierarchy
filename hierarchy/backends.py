from django.contrib.auth.backends import BaseBackend

from .services import get_permission_strings_for_user


class MPTTGroupBackend(BaseBackend):
    """

    """
    def get_group_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return get_permission_strings_for_user(user_obj)
