from django.db import models

from apps.utils.abs_model import AbstractBaseModel



class KinderGarten(AbstractBaseModel):
    """
    This model is used to store the information of the kindergartens
    """
    name = models.CharField(max_length=255)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='kindergartens')
    description = models.TextField(max_length=500, help_text='Max 500 characters')
    longitude = models.FloatField(null=True, blank=True, help_text='Longitude of the location')
    latitude = models.FloatField(null=True, blank=True, help_text='Latitude of the location')
    phone = models.CharField(max_length=255, help_text='Enter the phone number of the kindergarten')
    inn = models.CharField(max_length=255, help_text='Enter the INN of the kindergarten')

    def __str__(self):

        return self.name

    class Meta:
        verbose_name = 'Kinder Garden'
        verbose_name_plural = 'Kinder Gardens'


class KinderGartenCamera(AbstractBaseModel):
    """
    This model is used to store the information of the cameras that are installed in the kindergartens.
    Unique together with kindergarten and camera
    """
    kindergarten = models.ForeignKey(
        KinderGarten,
        on_delete=models.CASCADE,
        related_name='cameras'
    )
    camera = models.ForeignKey(
        'core.Camera',
        on_delete=models.CASCADE,
        related_name='kindergartens'
    )

    def __str__(self):
        return f'{self.kindergarten} - {self.camera}'

    class Meta:
        verbose_name = 'Kinder Garden Camera'
        verbose_name_plural = 'Kinder Garden Cameras'
        unique_together = ('kindergarten', 'camera')

