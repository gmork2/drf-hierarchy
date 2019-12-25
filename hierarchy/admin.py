from django.contrib import admin
from django import forms
from django.utils.translation import gettext as _
from django.utils.html import format_html

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
        'inheritable',
        'max_children',
        '_level'
    )
    search_fields = ('group',)
    fieldsets = (
        (None, {
            'fields': ('parent', 'group', 'max_children', 'inheritable')
        }),
    )
    list_display_links = ('indented_title',)

    def _level(self, instance):
        lvl = instance.parent.level + 1 if instance.parent else instance._mpttfield('level')
        return lvl

    _level.short_description = _('level')

    def indented_title(self, instance):
        lvl = self._level(instance)
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            lvl * self.mptt_level_indent,
            instance.group.name,
        )

    indented_title.short_description = _('group')


admin.site.register(MPTTGroup, MPTTGroupAdmin)
