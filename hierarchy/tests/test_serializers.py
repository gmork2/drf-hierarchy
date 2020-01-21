from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase

from hierarchy.serializers import MPTTGroupSerializer
from hierarchy.models import MPTTGroup


class MPTTGroupTestCase(APITestCase):
    def setUp(self):
        """

        """
        self.group_names = (
            '/', 'bin', 'dev', 'etc', 'home', 'lib', 'mnt', 'proc', 'root', 'home',
            'sbin', 'tmp', 'usr', 'cp', 'ksh', 'ls', 'pwd', 'passwd',
        )
        groups = [Group(name=n) for n in self.group_names]
        Group.objects.bulk_create(groups)

        self.root = MPTTGroup(group=Group.objects.get(name=self.group_names[0]))
        self.root.save()
