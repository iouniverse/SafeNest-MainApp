from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import UserProfileAPIView, SendOTPAPIView, VerifyOTPAPIView, \
    PhoneTokenObtainPairView

urlpatterns = [
    path('login/', PhoneTokenObtainPairView.as_view(), name='login-view'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),

    path('send-otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify'),
]
