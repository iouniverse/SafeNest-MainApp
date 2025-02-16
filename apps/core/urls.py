from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),
    path('screenshot/', views.ScreenshotAPIView.as_view(), name='screenshot'),
    path('record/', views.RecordAPIView.as_view(), name='record'),
]