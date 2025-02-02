import os

from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.serializers import UserCameraSerializer
from apps.participants.models import RepresentativeChildCamera as UserCamera


class HomeAPIView(APIView):
    """
    API endpoint that allows users to be viewed.
    Can only be accessed by authenticated users.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return UserCamera.objects.filter(representative_child__representative_id=1)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserCameraSerializer(queryset, many=True)

        cameras = serializer.data
        return Response({"cameras": cameras})


class M3U8FileAPIView(APIView):
    """
    API endpoint to serve the m3u8 stream files for cameras.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, file_name):
        camera_file_path = os.path.join('/var/lib/streams', file_name)

        print(camera_file_path)

        if os.path.exists(camera_file_path):
            return FileResponse(open(camera_file_path, 'rb'), content_type='application/vnd.apple.mpegurl')

        return Response({"error": "File not found"}, status=404)
