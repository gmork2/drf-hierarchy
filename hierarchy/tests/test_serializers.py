from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from hierarchy.models import MPTTGroup
from hierarchy.serializers import MPTTGroupSerializer


class MPTTGroupSerializerTestCase(APITestCase):
    def setUp(self):
        groups = [
            Group.objects.create(name="/"),
            Group.objects.create(name="etc"),
            Group.objects.create(name="nginx"),
            Group.objects.create(name="sites-enabled"),
        ]
        self.root = MPTTGroup.objects.create(group=groups[0])
        self.level_1 = MPTTGroup.objects.create(group=groups[1], parent=self.root)
        self.level_2 = MPTTGroup.objects.create(group=groups[2], parent=self.level_1)
        self.level_3 = MPTTGroup.objects.create(group=groups[3], parent=self.level_2)

    def test_children_are_limited_by_max_depth_context(self):
        serializer = MPTTGroupSerializer(self.root, context={"max_depth": 1})
        data = serializer.data

        self.assertEqual(len(data["children"]), 1)
        self.assertEqual(data["children"][0]["group"], self.level_1.group_id)
        self.assertEqual(data["children"][0]["children"], [])

    def test_children_are_serialized_recursively_with_default_depth(self):
        serializer = MPTTGroupSerializer(self.root)
        data = serializer.data

        self.assertEqual(data["children"][0]["group"], self.level_1.group_id)
        self.assertEqual(data["children"][0]["children"][0]["group"], self.level_2.group_id)
        self.assertEqual(
            data["children"][0]["children"][0]["children"][0]["group"],
            self.level_3.group_id,
        )
