from django.contrib import admin

from apps.participants.models import Child, Group, RepresentativeChild, Tariff

admin.site.register(Child)
admin.site.register(RepresentativeChild)
admin.site.register(Group)
admin.site.register(Tariff)
