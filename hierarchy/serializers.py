from rest_framework import serializers
from .models import MPTTGroup


class MPTTGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTGroup
        fields = ("id", "group",)
