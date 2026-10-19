from typing import Set

from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager

from . import settings as local_settings
from .validators import validate_max_children, validate_not_descendant_of_self, validate_not_parent_of_self


def get_sentinel_tree():
    """
    Point to deleted node parent.

    :return:
    """
    return Group.objects.first()


def get_permissions(
        root: 'MPTTGroup',
        method: str = local_settings.HIERARCHY_MPTT_METHOD,
        **kwargs) -> Set[int]:
    """
    Verify the permissions according to a tree path method.

    :param root:
    :param method:
    :param kwargs:
    :return:
    """
    perm_ids = set(root.group.permissions.values_list('id', flat=True))

    for node in getattr(root, method)(**kwargs):
        query = node.group.permissions.filter(group__hierarchy__inheritable=True)
        perm_ids.update(query.values_list('id', flat=True))

    return perm_ids


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

    @property
    def permissions(self, method: str = local_settings.HIERARCHY_MPTT_METHOD) -> QuerySet[Permission]:
        """
        Property that returns group permissions as queryset.

        Parameters
        ----------
        method: str

        Returns
        -------

        """
        perm_ids = get_permissions(self, method)
        return Permission.objects.filter(id__in=perm_ids)

    class Meta:
        unique_together = ('parent', 'group')
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = 'group'
