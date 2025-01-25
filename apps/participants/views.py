from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.participants.models import RepresentativeChild
from apps.participants.serializers import RepresentativeChildSerializer


class RepresentativeChildrenAPIView(APIView):
    """
    This view is used to get the children of the user that are represented by him.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RepresentativeChild.objects.filter(representative=self.request.user).select_related('child')

    def get(self, request):
        serializer = RepresentativeChildSerializer(self.get_queryset(), many=True)

        return Response({'children': [item['child'] for item in serializer.data]})
