from django.contrib import admin

from apps.core.models import Camera
from apps.kindergarten.models import Region, District
from apps.kindergarten.models.kindergarten import KinderGartenCamera, KinderGarten

admin.site.register(Region)
admin.site.register(District)



class KinderGartenCamerInlines(admin.TabularInline):
    """
    Tabular Inline View for KinderGartenCamera
    Extra is set to 0 to hide the add button
    """
    model = KinderGartenCamera
    extra = 0
    autocomplete_fields = ['camera']


@admin.register(KinderGarten)
class KinderGartenAdmin(admin.ModelAdmin):
    """
    Admin View for KinderGarten
    """
    inlines = [KinderGartenCamerInlines]
    list_display = ['name', 'district', 'phone', 'inn']
    search_fields = ['name', 'district__name', 'phone', 'inn']
    list_filter = ['district']

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    """
    Admin View for Camera
    """
    list_display = ['name', 'ip', 'port']
    search_fields = ['name', 'ip', 'port']
    list_filter = ['name', 'ip', 'port']