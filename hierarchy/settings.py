from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

MPTT_METHODS_LIST = (
    'get_ancestors', 'get_children', 'get_descendants', 'get_family', 'get_next_sibling',
    'get_previous_sibling', 'get_root', 'get_siblings',
)
HIERARCHY_MAX_CHILDREN = getattr(settings, 'HIERARCHY_MAX_CHILDREN', None)
HIERARCHY_MPTT_METHOD = getattr(settings, 'HIERARCHY_MPTT_METHOD', MPTT_METHODS_LIST[2])
HIERARCHY_MAX_SERIALIZATION_DEPTH = getattr(settings, 'HIERARCHY_MAX_SERIALIZATION_DEPTH', 5)

if HIERARCHY_MPTT_METHOD not in MPTT_METHODS_LIST:
    raise ImproperlyConfigured(
        f'HIERARCHY_MPTT_METHOD must be one of {MPTT_METHODS_LIST}. '
        f'Got: {HIERARCHY_MPTT_METHOD}'
    )
