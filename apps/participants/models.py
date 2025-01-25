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
        limit_choices_to={'ut': CustomUser.UserTypes.USER}
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
