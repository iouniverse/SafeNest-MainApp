from django.db import models

from apps.utils.abs_model import AbstractBaseModel


class Region(AbstractBaseModel):
    """
    Only the name of the region is stored in this model
    """
    name = models.CharField(max_length=255,help_text='Enter the name of the region')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class District(AbstractBaseModel):
    """
    Contains the name of the district and the region to which it belongs
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=255, help_text='Enter the name of the district')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'