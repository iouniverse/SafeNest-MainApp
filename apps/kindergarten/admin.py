from django.contrib import admin

from apps.core.models import Camera
from apps.kindergarten.models import Region, District
from apps.kindergarten.models.kindergarten import KinderGarden

admin.site.register(Region)
admin.site.register(District)




@admin.register(KinderGarden)
class KinderGardenAdmin(admin.ModelAdmin):
    """
    Admin View for KinderGarden
    """
    list_display = ['name', 'district', 'phone']
    search_fields = ['name', 'district__name', 'phone']
    list_filter = ['district']

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    """
    Admin View for Camera
    """
    list_display = ['name', 'ip', 'port']
    search_fields = ['name', 'ip', 'port']
    list_filter = ['name', 'ip', 'port']