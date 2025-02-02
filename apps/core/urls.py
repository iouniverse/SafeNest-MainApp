from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),
]