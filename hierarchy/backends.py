from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from .models import MPTTGroup


class MPTTGroupBackend(BaseBackend):
    """

    """
    def get_group_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        perms = set()

        for obj in MPTTGroup.objects.filter(**{user_groups_query: user_obj}):
            values = [
                '.'.join([str(ct), name])
                for ct, name in obj.permissions.values_list('content_type__app_label', 'codename')
            ]
            perms.update(values)

        return perms
