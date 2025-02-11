from rest_framework import serializers

from apps.participants.models import Child, RepresentativeChild, Tariff, UserTariff


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


class TariffSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Tariff
        fields = ['id', 'name', 'price', 'duration', 'payment_url']

    def get_payment_url(self, obj):
        return f"https://pay.yandex.ru/to/410012736276443?sum={obj.price}&label=123456789"


class UserTariffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tariff.id')
    name = serializers.CharField(source='tariff.name')
    price = serializers.IntegerField(source='tariff.price')
    duration = serializers.IntegerField(source='tariff.duration')


    class Meta:
        model = UserTariff
        fields = ['id', 'name', 'price', 'duration', 'start_date', 'end_date']
