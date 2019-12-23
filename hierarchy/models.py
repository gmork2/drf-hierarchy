from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager


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

    tree = TreeManager()

    def __str__(self):
        if self.id:
            ancestors = self.get_ancestors()
            return ' > '.join([force_text(i.group.name) for i in ancestors] + [self.group.name, ])
        return f'id={self.id}'

    def clean(self):
        """

        """
        if self.id:
            descendant_ids = self.get_descendants().values_list('id', flat=True)
            if self.parent and self.parent.id in descendant_ids:
                raise ValidationError(_("You can't set the parent of the "
                                        "item to a descendant."))
            if self.id == getattr(self.parent, 'id', None):
                raise ValidationError(_("You can't set the parent of the "
                                        "item to itself."))

    def save(self, *args, **kwargs):
        """
        Ensure that clean method is always called on save.
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('parent', 'group')
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        order_insertion_by = 'group'


