from django.conf import settings
from rest_framework import serializers

from apps.core.models import Screenshot, Recording
from apps.participants.models import RepresentativeChildCamera as UserCamera


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
        model = UserCamera

        fields = ['camera', 'low_quality_file', 'high_quality_file']

    def get_low_quality_file(self, obj):
        file_path = f"cameras/camera_{obj.camera.id}_low.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"

    def get_high_quality_file(self, obj):
        file_path = f"cameras/camera_{obj.camera.id}_high.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"


class ScreenshotSerializer(serializers.ModelSerializer):
    """
    Screenshot serializer for the user.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = Screenshot
        fields = ["id", "file", "description", "user"]


class RecordSerializer(serializers.ModelSerializer):
    """
    Record serializer for the user.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.FileField(required=True, allow_empty_file=False)

    class Meta:
        model = Recording
        fields = ["id", "file", "description", "user"]
