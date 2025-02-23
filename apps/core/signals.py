import os
import logging

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def delete_file(file):
    """
    Delete file function
    """
    if file and hasattr(file, 'path'):
        try:
            if os.path.isfile(file.path):
                os.remove(file.path)
        except Exception as e:
            print(f"Error deleting file {file.path}: {str(e)}")


@receiver(pre_delete)
def delete_file_screenshots_and_record(sender, instance, **kwargs):
    """
    Signal to delete files when a model instance is deleted.
    Works for all models that contain FileField or ImageField.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, (models.FileField, models.ImageField)):
            file = getattr(instance, field.name)
            delete_file(file)


@receiver(pre_save)
def delete_old_screenshots_and_record(sender, instance, **kwargs):
    """
    Delete the old file before updating the object.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, (models.FileField, models.ImageField)):
            try:
                old_file = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return

            old_file = getattr(old_file, field.name)
            new_file_field = getattr(instance, field.name)

            if old_file and old_file != new_file_field:
                delete_file(old_file)
