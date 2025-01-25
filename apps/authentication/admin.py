from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.authentication.models.otp import PhoneToken

admin.site.register(PhoneToken)
admin.site.register(get_user_model())