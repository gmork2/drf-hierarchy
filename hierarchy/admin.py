from django.contrib import admin
from django import forms

from .models import MPTTGroup


class MPTTGroupAdminForm(forms.ModelForm):
    class Meta:
        model = MPTTGroup
        fields = '__all__'


class MPTTGroupAdmin(admin.ModelAdmin):
    form = MPTTGroupAdminForm
    list_display = ('group',)
    search_fields = ('group',)
    fieldsets = (
        (None, {
            'fields': ('parent', 'group',)
        }),
    )


admin.site.register(MPTTGroup, MPTTGroupAdmin)
