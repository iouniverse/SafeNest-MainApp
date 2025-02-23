from django.db import models

from apps.utils.abs_model import AbstractBaseModel


class KinderGarden(AbstractBaseModel):
    """
    This model is used to store the information of the kindergartens.
    """
    name = models.CharField(max_length=255)
    district = models.ForeignKey('kindergarten.District', on_delete=models.CASCADE, related_name='kindergartens')
    longitude = models.FloatField(null=True, blank=True, help_text='Longitude of the location')
    latitude = models.FloatField(null=True, blank=True, help_text='Latitude of the location')
    phone = models.CharField(max_length=12, help_text='Enter the phone number of the kindergarten')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kinder Garden'
        verbose_name_plural = 'Kinder Gardens'
        db_table = 'kinder_garden'
