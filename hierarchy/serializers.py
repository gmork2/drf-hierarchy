from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission

from rest_framework import serializers

from .models import MPTTGroup


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RecursiveField(serializers.BaseSerializer):
    """
    Create instance for serializer parent and returns serialized
    data.
    """
    def to_representation(self, value):
        parent_serializer = self.parent.parent.__class__
        serializer = parent_serializer(value, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        parent_serializer = self.parent.parent.__class__
        model_class = parent_serializer.Meta.model
        try:
            instance = model_class.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Object {0} not found".format(
                    model_class().__class__.__name__
                )
            )
        return instance


class MPTTGroupSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = MPTTGroup
        fields = (
            'id', 'group', 'parent', 'children', 'permissions', 'inheritable',
            'max_children'
        )
