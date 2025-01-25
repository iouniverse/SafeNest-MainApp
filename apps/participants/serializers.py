from rest_framework import serializers

from apps.participants.models import Child, RepresentativeChild


class ChildSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the children of the user
    """

    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'age']


class RepresentativeChildSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the children of the user
    """
    child = ChildSerializer()

    class Meta:
        model = RepresentativeChild
        fields = ['child']
