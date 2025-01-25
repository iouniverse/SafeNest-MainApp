import re
import random

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.utils.abs_model import AbstractBaseModel


class PhoneToken(AbstractBaseModel):
    """
    PhoneToken model for OTP verification of phone number.
    AbstractBaseModel is a custom abstract model that contains
    """
    phone_number = models.CharField(max_length=12, unique=True)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        # Generate a random 6-digit OTP
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def is_expired(self):
        # Check if the OTP is expired since it was created
        return (timezone.now() - self.created_at).total_seconds() > 60 * settings.OTP_EXPIRY

    def clean_phone_number(self):
        """
        Remove all non-numeric characters from the phone number.
        Check if the operator code is valid
        """
        phone_number = re.sub(r'\D', '', self.phone_number.strip())
        valid_operators = settings.VALID_OPERATORS_PHONE
        operator_code = phone_number[3:5]

        if operator_code not in valid_operators:
            raise ValidationError("Invalid operator code.")

        return phone_number

    def clean(self):
        # Clean the phone number field
        self.phone_number = self.clean_phone_number()
        super().clean()

    def __str__(self):
        return f'{self.phone_number} - {self.otp}'

    class Meta:
        verbose_name = 'Phone Token'
        verbose_name_plural = 'Phone Tokens'
