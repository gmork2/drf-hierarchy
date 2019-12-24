from django.conf import settings


HIERARCHY_MAX_CHILDREN = getattr(settings, 'HIERARCHY_MAX_CHILDREN', None)
HIERARCHY_MPTT_METHOD = getattr(settings, 'HIERARCHY_MPTT_METHOD', 'get_descendants')
