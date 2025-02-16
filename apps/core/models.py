from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.kindergarten.models import KinderGarden
from apps.participants.models import Group
from apps.utils.abs_model import AbstractBaseModel


class Camera(AbstractBaseModel):
    """
    Represents a Camera configuration within a system.

    Attributes:
        garden: ForeignKey relationship pointing to the KinderGarden that this camera is
            associated with.
        group: ForeignKey relationship pointing to the Group that this camera is optionally
            associated with. Can be null if no group is linked.
        name: The name of the camera as a string.
        ip: The IP address of the camera.
        port: The port number on which the camera is accessible.
        username: The username required for accessing the camera.
        password: The password required for accessing the camera.
        status: A boolean flag indicating whether the camera is active or not.

    Meta:
        verbose_name: The human-readable name of the camera entity.
        verbose_name_plural: The human-readable plural name of the camera entity.
        db_table: The database table name for the camera entity.
    """
    garden = models.ForeignKey(
        KinderGarden,
        on_delete=models.CASCADE,
        related_name='cameras'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='cameras',
        null=True
    )
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField()

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.ip}:{self.port}'

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        db_table = 'camera'


class Screenshot(AbstractBaseModel):
    """
    Represents a screenshot uploaded by a user, containing details about the image and its metadata.

    Meta:
        verbose_name (str): Human-readable name of the model in singular form, "Screenshot".
        verbose_name_plural (str): Human-readable name of the model in plural form, "Screenshots".
        db_table (str): Name of the database table associated with this model, "screenshot".
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='screenshots/%Y/%m/%d',
        help_text='Please upload a screenshot image',
        validators=[FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)]
    )
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.user} - {self.description}'

    class Meta:
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'
        db_table = 'screenshot'


class Recording(AbstractBaseModel):
    """
    Represents a Recording model for managing user-uploaded recordings.

    Meta:
        verbose_name (str): A human-readable singular name of the model for
            admin purposes.
        verbose_name_plural (str): A plural human-readable name of the model
            for admin purposes.
        db_table (str): Specifies the database table name for the model.
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
        db_table = 'recording'
