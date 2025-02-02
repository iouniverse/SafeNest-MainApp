from django.conf import settings
from rest_framework import serializers

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
        file_path = f"cameras/camera_{obj.camera.id}_0.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"

    def get_high_quality_file(self, obj):
        file_path = f"cameras/camera_{obj.camera.id}_1.m3u8"
        return f"{settings.MEDIA_URL}{file_path}"
