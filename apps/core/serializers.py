from django.conf import settings
from rest_framework import serializers

from apps.core.models import Screenshot, Recording, Camera


# from apps.participants.models import RepresentativeChildCamera as UserCamera


class UserCameraSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserCamera model.

    Methods:
        get_low_quality_file(self, obj)
            Generates the file name for the low-quality video file corresponding to a specific camera.
        get_high_quality_file(self, obj)
            Generates the file name for the high-quality video file corresponding to a specific camera.
    """
    low_quality_file = serializers.SerializerMethodField()
    high_quality_file = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ['low_quality_file', 'high_quality_file']

    @staticmethod
    def get_low_quality_file(obj):
        file_path = f"cameras/camera_{obj.id}_low.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"

    @staticmethod
    def get_high_quality_file(obj):
        file_path = f"cameras/camera_{obj.id}_high.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"


class ScreenshotSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Screenshot model.

    Attributes:
        user: A hidden field that automatically sets the current user as the
            value.
        file: An image field that requires a file to be provided and doesn't allow
            empty files.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = Screenshot
        fields = ["id", "file", "description", "user"]


class RecordSerializer(serializers.ModelSerializer):
    """
    This class is a serializer for the Recording model.

    Attributes:
        user: Represents the currently authenticated user. This is a hidden
              field that automatically uses the CurrentUserDefault.
        file: Represents the file to be uploaded. This field is mandatory, and
              empty uploads are not allowed.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.FileField(required=True, allow_empty_file=False)

    class Meta:
        model = Recording
        fields = ["id", "file", "description", "user"]
