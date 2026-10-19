from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import MPTTGroup
from .serializers import MPTTGroupSerializer


class MPTTGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MPTTGroupSerializer
    queryset = MPTTGroup.objects.none()

    def get_queryset(self):
        return (
            MPTTGroup.objects.filter(parent=None)
            .select_related('group', 'parent')
            .prefetch_related('group__permissions')
        )
