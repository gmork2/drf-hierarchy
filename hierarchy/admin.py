from django.contrib import admin
from django import forms

from mptt.admin import DraggableMPTTAdmin

from .models import MPTTGroup


class MPTTGroupAdminForm(forms.ModelForm):
    class Meta:
        model = MPTTGroup
        fields = '__all__'


class MPTTGroupAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    expand_tree_by_default = True
    form = MPTTGroupAdminForm
    list_display = (
        'tree_actions',
        'indented_title',
        'group',
    )
    search_fields = ('group',)
    fieldsets = (
        (None, {
            'fields': ('parent', 'group', 'max_children', 'inheritable')
        }),
    )


admin.site.register(MPTTGroup, MPTTGroupAdmin)
