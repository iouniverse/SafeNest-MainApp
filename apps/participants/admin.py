from django.contrib import admin

from apps.participants.models import Child, Group, Employee, RepresentativeChild, Tariff, UserTariff

# Register your models here.
admin.site.register(Child)
admin.site.register(RepresentativeChild)
admin.site.register(Group)
admin.site.register(Employee)
admin.site.register(Tariff)
admin.site.register(UserTariff)