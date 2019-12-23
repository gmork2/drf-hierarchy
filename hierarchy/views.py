from rest_framework import viewsets

from .models import MPTTGroup
from .serializers import MPTTGroupSerializer


class MPTTGroupViewSet(viewsets.ModelViewSet):
    queryset = MPTTGroup.objects.all()
    serializer_class = MPTTGroupSerializer
