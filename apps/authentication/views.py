from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.authentication.models.otp import PhoneToken
from apps.authentication.serializers import RegisterSerializer


# class RegisterAPIView(CreateAPIView):
#     """
#     User register view
#     """
#
#     permission_classes = ()
#     authentication_classes = ()
#     serializer_class = RegisterSerializer
#
#     def perform_create(self, serializer):
#         pass


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
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update PhoneToken
        phone_token, created = PhoneToken.objects.get_or_create(phone_number=phone_number)
        phone_token.generate_otp()

        # send_sms(phone_number, phone_token.otp)

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    """
    Verify OTP for phone number using PhoneToken model
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Verify OTP for phone number using PhoneToken model and set verified to True.
        Phone number and otp are required in the request data.
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

        phone_token.verified = True
        phone_token.save()

        return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)


class RegisterAPIView(CreateAPIView):
    """
    User register view with phone number verification
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        """
        Perform create method for RegisterAPIView.
        Check if phone number is verified before saving user.
        """
        phone_number = self.request.data.get("phone_number")
        try:
            phone_token = PhoneToken.objects.get(phone_number=phone_number)
        except PhoneToken.DoesNotExist:
            raise ValidationError({"phone_number": "Phone number not found"})

        if not phone_token.verified:
            raise ValidationError({"phone_number": "Phone number not verified"})

        serializer.save()

        # phone_token.delete()


class UserProfileAPIView(APIView):
    """
    User profile view with first name, last name, and phone number
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
        })
