from rest_framework import serializers

from apps.participants.models import RepresentativeChildCamera as UserCamera


class UserCameraSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name')
    camera_id = serializers.IntegerField(source='camera.id')
    camera_status = serializers.BooleanField(source='camera.status')

    m3u8_url = serializers.SerializerMethodField()

    class Meta:
        model = UserCamera
        fields = ('camera_name', 'm3u8_url', 'camera_id', 'camera_status')

    @staticmethod
    def get_m3u8_url(obj):
        return f"/content/stream/get_m3u8_url/camera_{obj.camera_id}.m3u8"
