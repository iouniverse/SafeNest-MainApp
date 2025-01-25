from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.views import RegisterAPIView, UserProfileAPIView, SendOTPAPIView, VerifyOTPAPIView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login-view'),
    path('register/', RegisterAPIView.as_view(), name='register-view'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),

    path('send-otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify'),
]
