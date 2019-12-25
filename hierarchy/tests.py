from unittest import skip

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from .models import MPTTGroup
from .settings import MPTT_METHODS_LIST


class MPTTGroupTestCase(TestCase):
    def setUp(self):
        """

        """
        self.group_names = ('/', 'etc', 'usr', 'local', 'share', 'man',)
        groups = [Group(name=n) for n in self.group_names]
        Group.objects.bulk_create(groups)

        self.root = MPTTGroup(group=Group.objects.get(name=self.group_names[0]))
        self.root.save()

    def test_mptt_methods_list(self):
        """
        Check if all mptt methods are available.
        """
        for method in MPTT_METHODS_LIST:
            self.assertTrue(hasattr(self.root, method))

    def test_circular_reference(self):
        """
        Prevent simple circular reference.
        """
        local = Group.objects.get(name=self.group_names[3])
        node = MPTTGroup.objects.create(group=local, parent=self.root)
        self.root.parent = node

        self.assertRaises(ValidationError, self.root.clean)

    def test_multi_level_circular_reference(self):
        """
        Prevent multi-level circular reference.

        :return:
        """
        node = None
        for name in self.group_names[1:]:
            group = Group.objects.get(name=name)
            if node is None:
                node = MPTTGroup.objects.create(group=group, parent=self.root)
            else:
                node = MPTTGroup.objects.create(group=group, parent=node)
        self.root.parent = node

        self.assertRaises(ValidationError, self.root.clean)

    def test_set_parent_itself(self):
        """
        Prevent set parent to itself.
        """
        local = Group.objects.get(name=self.group_names[3])
        node = MPTTGroup.objects.create(group=local)
        node.parent = node

        self.assertRaises(ValidationError, node.clean)
