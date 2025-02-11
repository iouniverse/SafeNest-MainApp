from django.urls import path

from apps.participants.views import RepresentativeChildrenAPIView

urlpatterns = [
    path('', RepresentativeChildrenAPIView.as_view(), name='user-children-list'),
]