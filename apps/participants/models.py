from django.db import models


class Employee(models.Model):
    """
    This model is used to store the information of the employees
    """
    class PositionStatus(models.TextChoices):
        INTERN = 'Intern',
        JUNIOR = 'Junior',
        MIDDLE = 'Middle',
        MANAGER = 'Manager',
        DIRECTOR = 'Director'

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


class Group(models.Model):
    """
    This model is used to store the information of the groups
    """
    name = models.CharField(max_length=255)
    limit = models.IntegerField()
    first_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    second_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

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
        on_delete=models.CASCADE,
        related_name='children'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Children'
