from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.models import PhoneToken, User
from apps.authentication.serializers import RegisterSerializer, PhoneTokenObtainPairSerializer
from apps.utils.send_sms import send_sms


class SendOTPAPIView(APIView):
    """
    Send OTP to user's phone number using PhoneToken model
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Send OTP to user's phone number using PhoneToken model.
        """
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(phone_number) != 12:
            return Response(
                {"error": "Phone number must be 12 digits"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create or update PhoneToken
        phone_token, created = PhoneToken.objects.get_or_create(phone_number=phone_number)
        if phone_token.is_expired():
            phone_token.delete()
            phone_token = PhoneToken.objects.create(phone_number=phone_number)

        phone_token.generate_otp()

        # send_sms(phone_number, f"https://star-one.uz/ Tasdiqlash kodi {phone_token.otp} !!!!")

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    """
    Verify OTP for phone number using PhoneToken model
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Handles the verification of OTP for phone numbers provided by users. Upon successful verification, returns
        authentication tokens. This endpoint ensures the validity and expiration of OTP codes, and verifies if the
        phone number is already confirmed.

        Arguments:
            request: The HTTP request object, containing the data input by the client.
            *args: Positional arguments forwarded to the method.
            **kwargs: Keyword arguments forwarded to the method.

        Returns:
            Response: HTTP response with a status code and message. If verification is successful, provides the
            authentication tokens; otherwise, returns descriptive error messages.

        Raises:
            None

        """
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if not phone_number or not otp:
            return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            phone_token = PhoneToken.objects.get(phone_number=phone_number)
        except PhoneToken.DoesNotExist:
            return Response({"error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)

        if phone_token.verified:
            return Response({"message": "Phone number already verified"}, status=status.HTTP_400_BAD_REQUEST)

        if phone_token.is_expired():
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        if phone_token.otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response({"error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        phone_token.verified = True
        phone_token.save()

        return Response({
            "message": "Phone number verified successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),

        }, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    """
    Handles user profile retrieval for authenticated users.

    This view allows an authenticated user to retrieve their profile information
    including first name, last name, phone number, and profile picture.

    Attributes:
        permission_classes: A list that specifies the permissions required to
                            access this view.
        authentication_classes: A list that specifies the authentication
                                mechanisms used for this view.

    Methods:
        get(request): Returns the profile details of the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get user profile with first name, last name, and phone number
        """
        user = request.user
        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "profile_picture": user.avatar.url if user.avatar else None,
        })


# class PhoneTokenObtainPairView(TokenObtainPairView):
#     """
#     Custom TokenObtainPairView to return access token with refresh token
#     """
#     serializer_class = PhoneTokenObtainPairSerializer
