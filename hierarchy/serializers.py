from django.contrib.auth.models import Permission
from rest_framework import serializers

from . import settings as local_settings
from .models import MPTTGroup


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class MPTTGroupSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = MPTTGroup
        fields = (
            "id",
            "group",
            "parent",
            "children",
            "permissions",
            "inheritable",
            "max_children",
        )

    def get_children(self, obj):
        current_depth = self.context.get("_depth", 0)
        max_depth = self.context.get("max_depth", local_settings.HIERARCHY_MAX_SERIALIZATION_DEPTH)
        if max_depth is not None and current_depth >= max_depth:
            return []

        children_queryset = obj.get_children().select_related("group", "parent")
        child_context = {**self.context, "_depth": current_depth + 1}
        serializer = self.__class__(children_queryset, many=True, context=child_context)
        return serializer.data
