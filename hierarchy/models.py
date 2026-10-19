from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models import QuerySet
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from . import settings as local_settings
from .services import get_permission_ids_for_node
from .validators import (
    validate_max_children,
    validate_not_descendant_of_self,
    validate_not_parent_of_self,
)


def get_sentinel_tree():
    """
    Point to deleted node parent.

    :return:
    """
    return Group.objects.first()


class MPTTGroup(MPTTModel):
    """
    Modified pre-order tree traversal of groups where permissions
    for each one can be inherit according to hierarchy order.
    """
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('parent'),
    )

    group = models.OneToOneField(
        Group,
        verbose_name=_('group'),
        blank=True,
        on_delete=models.SET(get_sentinel_tree),
        help_text=_(
            'The group this node relates to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="hierarchy_set",
        related_query_name="hierarchy",
    )
    propagate = models.BooleanField(default=True)
    inheritable = models.BooleanField(
        default=True,
        help_text=_(
            'Set group permissions as inheritable for others nodes. '
            'Provide a value to HIERARCHY_MPTT_METHOD to establish inheritance criteria.'
        )
    )
    max_children = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_(
            'Maximum number of children for this node'
        )
    )
    active = models.BooleanField(default=True)
    tree = TreeManager()

    def __str__(self):
        if self.id:
            ancestors = self.get_ancestors()
            return ' > '.join([force_str(i.group.name) for i in ancestors] + [self.group.name, ])
        return f'id={self.id}'

    def clean(self) -> None:
        """

        Returns
        -------

        """
        validate_max_children(self, self.max_children)
        validate_not_descendant_of_self(self)
        validate_not_parent_of_self(self)

    def save(self, *args, **kwargs):
        """
        Ensure that clean method is always called on save.

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        self.clean()
        super().save(*args, **kwargs)

    def get_permissions_queryset(self, method: str = local_settings.HIERARCHY_MPTT_METHOD, **kwargs) -> QuerySet[Permission]:
        """
        Returns group permissions as queryset.

        Parameters
        ----------
        method: str

        Returns
        -------

        """
        permission_ids = get_permission_ids_for_node(self, method=method, **kwargs)
        return Permission.objects.filter(id__in=permission_ids)

    @property
    def permissions(self) -> QuerySet[Permission]:
        return self.get_permissions_queryset()

    class Meta:
        unique_together = ('parent', 'group')
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = 'group'
