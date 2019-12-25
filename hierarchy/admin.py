from django.contrib import admin
from django import forms
from django.utils.translation import gettext as _

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
        'max_children'
    )
    search_fields = ('group',)
    fieldsets = (
        (None, {
            'fields': ('parent', 'group', 'max_children', 'inheritable')
        }),
    )
    list_display_links = ('indented_title',)

    def indented_title(self, instance):
        from django.utils.html import format_html
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.group.name,
        )

    indented_title.short_description = _('group')


admin.site.register(MPTTGroup, MPTTGroupAdmin)
