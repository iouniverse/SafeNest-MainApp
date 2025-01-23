from django.conf import settings
from django.db import models

from apps.utils.abs_model import AbstractBaseModel


class Camera(AbstractBaseModel):
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'

class CameraUser(AbstractBaseModel):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='users')

    # This is a user id from the auth_user table in microservices project
    # it should be written like this: user_id = models.IntegerField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cameras')

    def __str__(self):
        return f'{self.camera} - {self.user}'

    class Meta:
        verbose_name = 'Camera User'
        verbose_name_plural = 'Camera Users'
        unique_together = ('camera', 'user')
