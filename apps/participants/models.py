from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.abs_model import AbstractBaseModel


class Group(models.Model):
    """
    This model is used to store the information of the groups
    """
    garden = models.ForeignKey(
        'kindergarten.KinderGarden',
        on_delete=models.PROTECT,
        related_name='groups'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: {self.garden.name}'

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        db_table = 'garden_group'


class Child(models.Model):
    """
    This model is used to store the information of the children
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name='children',
    )
    birth_certificate_series = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Child',
        verbose_name_plural = 'Children'
        db_table = 'child'


class RepresentativeChild(AbstractBaseModel):
    """
    This model is used to store the information of the children representatives.
    """
    representative = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='children',
    )
    child = models.ForeignKey(
        to=Child,
        on_delete=models.PROTECT,
        related_name='representatives'
    )
    end_date = models.DateField(null=True, blank=True)
    payment_status = models.BooleanField(default=False, editable=True) # temporary

    def clean(self):
        """
        Check if the user is already a representative of the child.
        Check if the child already has 2 representatives.
        """
        if RepresentativeChild.objects.filter(representative=self.representative, child=self.child).exists():
            raise ValueError(_('The user is already a representative of the child'))

        if RepresentativeChild.objects.filter(child=self.child).count() >= 2:
            raise ValueError(_('This child already has 2 representatives'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.representative.phone_number} - {self.child.first_name} {self.child.last_name}'

    class Meta:
        verbose_name = 'Child Representative',
        verbose_name_plural = 'Children Representatives'
        db_table = 'representative_child'


class Tariff(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)

    price = models.DecimalField(max_digits=15, decimal_places=2, help_text='Price of the tariff in UZS')
    sale_percent = models.PositiveSmallIntegerField(help_text='Sale percent')
    duration = models.PositiveSmallIntegerField(help_text='Duration of the tariff in days')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tariff'
        verbose_name_plural = 'Tariffs'
        ordering = ['-created_at']
        db_table = 'rate'
