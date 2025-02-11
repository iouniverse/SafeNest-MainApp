from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import CustomUser
from apps.utils.abs_model import AbstractBaseModel


class Employee(AbstractBaseModel):
    """
    This model is used to store the information of the employees
    """

    class PositionStatus(models.TextChoices):
        INTERN = 'Intern',
        JUNIOR = 'Junior',
        MIDDLE = 'Middle',
        MANAGER = 'Manager',
        DIRECTOR = 'Director',

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=255)
    position = models.CharField(
        max_length=255,
        choices=PositionStatus.choices,
        default=PositionStatus.INTERN
    )
    experience = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    # otpuska = models.IntegerField() # days of vacation

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Employee',
        verbose_name_plural = 'Employees'


class Group(models.Model):
    """
    This model is used to store the information of the groups
    """
    kindergarten = models.ForeignKey(
        'kindergarten.KinderGarten',
        on_delete=models.PROTECT,
        related_name='groups'
    )
    name = models.CharField(max_length=255)
    limit = models.IntegerField()
    first_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='first_employee'
    )
    second_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='second_employee'
    )

    def __str__(self):
        return f'{self.name}: {self.kindergarten.name}'

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Child(models.Model):
    """
    This model is used to store the information of the children
    """
    kindergarten = models.ForeignKey(
        'kindergarten.KinderGarten',
        on_delete=models.CASCADE,
        related_name='children'
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(default=2)
    birth_date = models.DateField(null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name='children',
    )

    def clean(self):
        if self.kindergarten_id != self.group.kindergarten_id:
            raise ValueError('The group should be in the same kindergarten as the child')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Child',
        verbose_name_plural = 'Children'


class RepresentativeChild(AbstractBaseModel):
    """
    This model is used to store the information of the children representatives.
    """

    class StatusRepresentative(models.TextChoices):
        """
        Status of the representative
        """
        PARENT = 'Parent'
        GUARDIAN = 'Guardian'

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

    status = models.CharField(
        max_length=10,
        choices=StatusRepresentative.choices,
        default=StatusRepresentative.PARENT
    )
    payment_status = models.BooleanField(default=False, editable=False)

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


class RepresentativeChildCamera(AbstractBaseModel):
    """
    This model is used to link RepresentativeChild with Camera.
    """
    representative_child = models.ForeignKey(
        to=RepresentativeChild,
        on_delete=models.CASCADE,
        related_name='cameras'
    )
    camera = models.ForeignKey(
        to='core.Camera',
        on_delete=models.CASCADE,
        related_name='representative_children'
    )

    def __str__(self):
        return f'{self.representative_child} - {self.camera}'

    class Meta:
        verbose_name = 'Representative Child Camera'
        verbose_name_plural = 'Representative Child Cameras'
        unique_together = ('representative_child', 'camera')


class Tariff(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)

    price = models.IntegerField(help_text='Price of the tariff in UZS')

    duration = models.IntegerField(help_text='Duration of the tariff in days')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tariff'
        verbose_name_plural = 'Tariffs'
        ordering = ['-created_at']


class UserTariff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tariffs')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='users')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        If is_paid is True, end_date will be automatically changed.
        """
        if self.is_paid and not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.tariff.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_id} - {self.tariff.name}, ({self.start_date} - {self.end_date})'

    class Meta:
        verbose_name = 'User Tariff'
        verbose_name_plural = 'User Tariffs'
        unique_together = ('user', 'tariff')
        ordering = ['-start_date']
