from rest_framework.generics import CreateAPIView

from apps.authentication.serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    """
    User register view
    """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        pass
