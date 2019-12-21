from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from .models import MPTTGroup


class MPTTGroupTestCase(TestCase):
    def setUp(self):
        """

        """
        group_names = ('etc', 'usr', 'local', 'share', 'man',)

        groups = [Group(name=n) for n in group_names]
        Group.objects.bulk_create(groups)
        for node in [MPTTGroup(group=g) for g in Group.objects.all()]:
            node.save()

    def test_circular_reference(self):
        """
        Prevent simple circular reference.
        """
        usr = MPTTGroup.objects.get(group=Group.objects.get(name="usr"))
        local = MPTTGroup.objects.get(group=Group.objects.get(name="local"))
        local.parent = usr
        local.save()

        usr.parent = local
        # usr = MPTTGroup.objects.get(group=Group.objects.get(name="usr"))
        # print(usr.get_descendants().values_list('id', flat=True))

        self.assertRaises(ValidationError, usr.save)

    def test_set_parent_itself(self):
        """
        Prevent set parent to itself.
        """
        group = Group.objects.get(name="etc")
        etc = MPTTGroup.objects.get(group=group)
        etc.parent = etc

        self.assertRaises(ValidationError, etc.save)
