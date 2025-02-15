import os
from datetime import date

from django.core.serializers import get_serializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models import Screenshot, Recording
from apps.core.serializers import UserCameraSerializer, ScreenshotSerializer, RecordSerializer
from apps.participants.models import RepresentativeChild, RepresentativeChildCamera as UserCamera, Tariff, UserTariff
from apps.participants.serializers import TariffSerializer, UserTariffSerializer


class HomeAPIView(APIView):
    """
    API endpoint that allows users to be viewed.
    Can only be accessed by authenticated users.
    """

    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self, representative_child: object):
        return UserCamera.objects.filter(representative_child=representative_child)

    def get_active_tariff(self, user):
        active_tariff = (
            UserTariff.objects.filter(user=user, end_date__gte=date.today())
            .order_by("-end_date")
            .first()
        )
        return active_tariff if active_tariff else None

    def get(self, request):
        user = request.user
        child_id = request.query_params.get('child_id')

        if not child_id:
            return Response({"error": "Child ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not child_id.isdigit():
            return Response({"error": "Child ID must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        if child_id == '0':
            return Response({"error": "Child ID cannot be 0"}, status=status.HTTP_400_BAD_REQUEST)

        representative_child = get_object_or_404(
            RepresentativeChild, id=child_id, representative=user
        )
        active_tariff = self.get_active_tariff(user)

        if not representative_child.payment_status:
            tariffs = Tariff.objects.filter(is_active=True)
            tariff_serializer = TariffSerializer(tariffs, many=True)
            return Response({
                "error": "User has not paid for the child",
                "message": "Please select a tariff to continue using the service",
                "tariffs": tariff_serializer.data,

            },
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        try:
            queryset = self.get_queryset(representative_child).select_related('camera')
        except RepresentativeChild.DoesNotExist:
            return Response(
                {"error": "Child not found or not associated with user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserCameraSerializer(queryset, many=True)

        return Response(
            {
                "cameras": serializer.data,
                "current_tariff": UserTariffSerializer(active_tariff).data if active_tariff else None,
            }
        )


class ScreenshotAPIView(APIView):
    """
    All Screenshot API endpoints for a user is accessible by authenticated users.
    Create Screenshot object and save it to the database.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = Screenshot.objects.filter(user=user)
        serializer = ScreenshotSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ScreenshotSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": "Screenshot saved successfully"
            },
            status=status.HTTP_201_CREATED
        )


class RecordAPIView(APIView):
    """
    All Record API endpoints for a user is accessible by authenticated users.
    Create Record object and save it to the database.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = Recording.objects.filter(user=user)
        serializer = RecordSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RecordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": "Recording saved successfully"
            },
        )
