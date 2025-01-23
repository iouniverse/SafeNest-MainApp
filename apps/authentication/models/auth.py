import re

from django.db import models
from django.conf import settings

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifiers
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create User with phone_number and password
        """
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(phone_number=phone_number, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError('The Password field must be set')

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create a superuser with phone_number and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    Custom user model where phone_number is the unique identifiers
    :param first_name: First name of the user
    :param last_name: Last name of the user
    :param avatar: Avatar of the user
    :param phone_number: Phone number of the user
    :param ut: Type of the user
    """
    class UserTypes(models.IntegerChoices):
        """
        User types for the CustomUser model
        """
        USER = 1, 'User'
        ADMIN = 2, 'Admin'
        SUPERUSER = 3, 'SuperUser'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^998\d{9}$',
                message='Phone number must be a valid Uzbekistan number starting with 998 and 12 digits long',
                code='invalid_phone_number'
            ),
        ]
    )
    ut = models.IntegerField(choices=UserTypes.choices, default=UserTypes.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def clean(self):
        """
        Clean the phone number field of the CustomUser model
        """
        self.phone_number = re.sub(r'\D', '', self.phone_number.strip())

        valid_operators = settings.VALID_OPERATORS_PHONE
        operator_code = self.phone_number[3:5]
        if operator_code not in valid_operators:
            raise ValidationError("Invalid operator code.")

        super().clean()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
