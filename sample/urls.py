from django.contrib import admin
from django.urls import path

from rest_framework import routers

from hierarchy.views import MPTTGroupViewSet


router = routers.DefaultRouter()
router.register('mpttgroup', MPTTGroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = urlpatterns + router.urls
