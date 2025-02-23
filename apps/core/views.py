import psutil
import hashlib

from collections import defaultdict

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models import Camera, RecordItem
from apps.participants.serializers import TariffSerializer
from apps.participants.models import RepresentativeChild, Tariff
from apps.core.serializers import UserCameraSerializer, RecordItemSerializer
from apps.utils.record_cameras import record_camera_stream, is_stream_running, stop_process


class HomeAPIView(APIView):
    """
    Represents the Home API endpoint for managing camera streams and tariffs.

    This class provides functionality for retrieving cameras associated with a child's
    group, checking tariff payment status, and stopping ongoing camera streams. It
    ensures that only authenticated users with valid JWT tokens can access its
    functionality. The class integrates methods for both GET and POST requests to handle
    different operations related to camera management and user interaction with the service.

    Attributes:
        permission_classes (list): Permissions required to access the API view.
        authentication_classes (list): Authentication mechanisms required to access the API view.

    Methods:
        get_active_tariff(): Returns active tariff objects from the database.

        get_queryset(representative_child): Fetches cameras associated with the given
        representative child's group and prepares their streaming URLs.

        get(request): Handles the GET request to fetch user cameras and ensure the user
        has an active payment tariff for the associated child.

        post(request, *args, **kwargs): Handles the POST request to stop running streams
        for all cameras associated with the user's child groups.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def get_active_tariff():
        return Tariff.objects.filter(is_active=True)

    def get_queryset(self, representative_child: object):
        cameras = Camera.objects.filter(group_id=representative_child.child.group_id)
        for camera in cameras:
            stream_hash = hashlib.md5(str(camera.id).encode()).hexdigest()
            camera.m3u8_url = f"{settings.MEDIA_URL}streams/{stream_hash}/index.m3u8"

        return cameras

    def get(self, request):
        user_id = request.user.id
        child_id = request.query_params.get('child_id')

        if not child_id:
            return Response({"error": "Child ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not child_id.isdigit():
            return Response({"error": "Child ID must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        if child_id == '0':
            return Response({"error": "Child ID cannot be 0"}, status=status.HTTP_400_BAD_REQUEST)
        representative_child = get_object_or_404(
            RepresentativeChild, child_id=child_id, representative=user_id
        )
        if not representative_child.payment_status:
            tariffs = self.get_active_tariff()
            tariff_serializer = TariffSerializer(tariffs, many=True)
            return Response({
                "error": "User has not paid for the child",
                "message": "Please select a tariff to continue using the service",
                "tariffs": tariff_serializer.data,
            }, status=status.HTTP_402_PAYMENT_REQUIRED)

        try:
            queryset = self.get_queryset(representative_child)
        except RepresentativeChild.DoesNotExist:
            return Response(
                {"error": "Child not found or not associated with user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserCameraSerializer(queryset, many=True)
        for camera in queryset:
            if camera.rtsp_url:
                record_camera_stream(camera.rtsp_url, camera.id)

        return Response(
            {
                "cameras": serializer.data,
                "current_tariff": TariffSerializer(self.get_active_tariff(), many=True).data
                if self.get_active_tariff() else None,
            }
        )

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        cameras = Camera.objects.filter(garden__groups__children__representatives__representative=user_id)

        stopped_streams = []
        for camera in cameras:
            if is_stream_running(str(camera.id)):
                stream_hash = hashlib.md5(str(camera.id).encode()).hexdigest()
                for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
                    try:
                        if "ffmpeg" in process.info["name"] and stream_hash in " ".join(process.info["cmdline"]):
                            stop_process(process)
                            stopped_streams.append(camera.id)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue

        return Response({"stopped_streams": stopped_streams}, status=status.HTTP_200_OK)


class RecordItemAPIView(APIView):
    """
    API View for managing RecordItem entities.

    This class provides API endpoints for retrieving and creating RecordItem
    objects. It handles GET and POST HTTP requests and uses JWT authentication
    and permissions to ensure secure access. The GET method retrieves all
    RecordItem instances associated with the authenticated user, and the POST
    method allows creating a new RecordItem instance.

    Attributes:
        permission_classes: Defines the permissions required to access this
            view. Only authenticated users are allowed.
        authentication_classes: Specifies the authentication mechanism used
            for validating requests. JWT-based authentication is implemented.

    Methods
    -------
    get(self, request, *args, **kwargs)
        Handles GET requests to retrieve a list of RecordItem objects
        associated with the authenticated user.

    post(self, request, *args, **kwargs)
        Accepts and validates record data from the request. Creates a new
        RecordItem instance on successful validation.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        data = RecordItem.objects.filter(user_id=user_id)

        grouped_data = defaultdict(list)
        for record in data:
            grouped_data[record.created_at.date().isoformat()].append({
                "id": record.id,
                "name": record.description
            })

        formatted_response = [
            {"date": key, "result": value} for key, value in grouped_data.items()
        ]
        return Response(formatted_response)

    def post(self, request, *args, **kwargs):
        serializer = RecordItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": "RecordItem saved successfully"
            },
            status=status.HTTP_201_CREATED
        )
