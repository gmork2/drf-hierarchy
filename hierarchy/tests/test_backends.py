from unittest import skip

from django.test import TestCase, override_settings
from django.contrib.auth.models import Group, Permission, User

from hierarchy.models import MPTTGroup


@override_settings(AUTHENTICATION_BACKENDS=['hierarchy.backends.MPTTGroupBackend'])
class GroupPermissionTestCase(TestCase):
    def setUp(self):
        """

        """
        data = ('test', 'test@example.com', 'test')
        self.user = User.objects.create_user(*data)
        self.admin = User.objects.create_superuser('admin', *data[1:])
        self.group = Group.objects.create(name='home')

        self.root = MPTTGroup(group=Group.objects.create(name='/'))
        self.root.save()

    def test_empty_tree(self):
        """

        :return:
        """
        permissions = self.user.get_group_permissions()
        self.assertEqual(permissions, set())

    def test_tree_without_users(self):
        """

        :return:
        """
        self.node = MPTTGroup.objects.create(group=self.group, parent=self.root)
        permissions = self.user.get_group_permissions()

        self.assertEqual(permissions, set())

        perm = Permission.objects.get(codename='change_user')
        self.group.permissions.add(perm)
        permissions = self.user.get_group_permissions()

        self.assertEqual(permissions, set())

    def test_tree_without_perms(self):
        """

        :return:
        """
        self.node = MPTTGroup.objects.create(group=self.group, parent=self.root)
        self.root.group.user_set.add(self.user)
        self.node.group.user_set.add(self.user)

        permissions = self.user.get_group_permissions()
        self.assertEqual(permissions, set())

    def test_simple_descendant_perms(self):
        """

        :return:
        """
        perm = Permission.objects.first()
        self.node = MPTTGroup.objects.create(group=self.group, parent=self.root)
        self.group.permissions.add(perm)

        self.root.group.user_set.add(self.user)

        permissions = self.user.get_group_permissions()
        perm_str = '.'.join([perm.content_type.app_label, perm.codename])

        self.assertEqual(permissions, {perm_str})
        self.assertTrue(self.user.has_perm(perm_str))
