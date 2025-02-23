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

    @property
    def rtsp_url(self):
        return f'rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/Streaming/Channels/101'

    def __str__(self):
        return f'{self.name} - {self.ip}:{self.port}'

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        db_table = 'camera'


class RecordItem(AbstractBaseModel):
    """
    Represents a Record Item in the system.

    Attributes:
        file (FileField): Represents the uploaded recording file. The field includes
            file validators and configures the path for storing uploaded files.
        is_video (BooleanField): Indicates whether the uploaded file is a video.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='recordings/%Y/%m/%d',
        help_text='Please upload a recording file',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov']
        )]
    )
    description = models.CharField(max_length=255, null=True)

    is_video = models.BooleanField()

    def __str__(self):
        return f'{self.id} - {self.description}'

    class Meta:
        verbose_name = 'Record Item'
        verbose_name_plural = 'Record Items'
        db_table = 'record_item'
