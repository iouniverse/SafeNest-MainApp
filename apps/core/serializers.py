import hashlib

from django.conf import settings
from rest_framework import serializers

from apps.core.models import RecordItem, Camera


class UserCameraSerializer(serializers.ModelSerializer):
    """
    Handles serialization of Camera objects with an additional field for high-quality
    file URL.

    Attributes:
        high_quality_file: A dynamically generated serializer method field that
        constructs a URL pointing to a high-quality video file for the camera object.

    Methods:
        get_high_quality_file(obj): Static method responsible for dynamically
        generating the high-quality file URL based on camera object properties.
    """
    high_quality_file = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ['high_quality_file']

    @staticmethod
    def get_high_quality_file(obj):
        file_path = hashlib.md5(str(obj.id).encode()).hexdigest()
        return f"{settings.MEDIA_URL}streams/{file_path}/index.m3u8"


class RecordItemSerializer(serializers.ModelSerializer):
    """
    Serializer handling the serialization and deserialization of RecordItem instances.

    Meta:
        model: RecordItem
            The model associated with this serializer.
        fields (List[str]): The list of model fields to include in the serialization.
            These fields are `["id", "file", "description", "user", "is_video"]`.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = RecordItem
        fields = ["id", "file", "description", "user", "is_video", "created_at"]
