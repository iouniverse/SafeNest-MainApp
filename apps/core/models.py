from django.conf import settings
from django.db import models

from apps.utils.abs_model import AbstractBaseModel


class Camera(AbstractBaseModel):
    """
    Camera model to store camera information
    """
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.ip}:{self.port}'

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'

