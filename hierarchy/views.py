from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import MPTTGroup
from .serializers import MPTTGroupSerializer


class MPTTGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = MPTTGroup.objects.filter(parent=None)
    serializer_class = MPTTGroupSerializer
