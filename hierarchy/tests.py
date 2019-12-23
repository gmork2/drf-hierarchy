from unittest import skip

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from .models import MPTTGroup


class MPTTGroupTestCase(TestCase):
    def setUp(self):
        """

        """
        self.group_names = ('/', 'etc', 'usr', 'local', 'share', 'man',)

        groups = [Group(name=n) for n in self.group_names]
        Group.objects.bulk_create(groups)

        # for node in [MPTTGroup(group=g) for g in Group.objects.all()]:
        #     node.save()
        self.root = MPTTGroup(group=Group.objects.get(name=self.group_names[0]))
        self.root.save()

    def test_circular_reference(self):
        """
        Prevent simple circular reference.
        """
        local = Group.objects.get(name=self.group_names[3])
        node = MPTTGroup.objects.create(group=local, parent=self.root)
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
