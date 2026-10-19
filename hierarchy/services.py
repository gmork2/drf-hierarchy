from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from . import settings as local_settings

if TYPE_CHECKING:
    from .models import MPTTGroup


def get_permission_ids_for_node(
    root: "MPTTGroup",
    method: str = local_settings.HIERARCHY_MPTT_METHOD,
    **kwargs,
) -> set[int]:
    traversal = getattr(root, method, None)
    if traversal is None or not callable(traversal):
        raise ImproperlyConfigured(f"Invalid hierarchy traversal method: {method}")

    permission_ids = set(root.group.permissions.values_list("id", flat=True))
    for node in traversal(**kwargs):
        if not node.inheritable:
            continue
        permission_ids.update(node.group.permissions.values_list("id", flat=True))
    return permission_ids


def get_permission_strings_for_user(user_obj) -> set[str]:
    from .models import MPTTGroup

    user_groups_field = get_user_model()._meta.get_field("groups")
    user_groups_query = f"group__{user_groups_field.related_query_name()}"
    permission_strings = set()

    queryset = (
        MPTTGroup.objects.filter(**{user_groups_query: user_obj})
        .select_related("group")
        .prefetch_related("group__permissions__content_type")
    )
    for hierarchy_group in queryset:
        values = hierarchy_group.get_permissions_queryset().values_list(
            "content_type__app_label",
            "codename",
        )
        permission_strings.update(f"{app_label}.{codename}" for app_label, codename in values)
    return permission_strings
