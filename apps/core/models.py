from django.conf import settings
from django.core.validators import FileExtensionValidator
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


class Screenshot(AbstractBaseModel):
    """
    Screenshot model for user.
    Check file extensions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='screenshots/%Y/%m/%d',
        help_text='Please upload a screenshot image',
        validators=[FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)]
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.description}'

    class Meta:
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'


class Recording(AbstractBaseModel):
    """
    Recording model for user.
    Check file extensions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='recordings/%Y/%m/%d',
        help_text='Please upload a recording file',
        validators=[FileExtensionValidator(allowed_extensions=settings.ALLOWED_VIDEO_EXTENSIONS)]
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.description}'

    class Meta:
        verbose_name = 'Recording'
        verbose_name_plural = 'Recordings'
