from django.conf import settings


MPTT_METHODS_LIST = (
    'get_ancestors', 'get_children', 'get_descendants', 'get_family', 'get_next_sibling',
    'get_previous_sibling', 'get_root', 'get_siblings',
)
HIERARCHY_MAX_CHILDREN = getattr(settings, 'HIERARCHY_MAX_CHILDREN', None)
HIERARCHY_MPTT_METHOD = getattr(settings, 'HIERARCHY_MPTT_METHOD', MPTT_METHODS_LIST[2])
