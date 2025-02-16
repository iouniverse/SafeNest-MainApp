from rest_framework import serializers

from apps.participants.models import Child, RepresentativeChild, Tariff


class ChildSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the children of the user
    """

    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name']


class RepresentativeChildSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the children of the user
    """
    child = ChildSerializer()

    class Meta:
        model = RepresentativeChild
        fields = ['child']


class TariffSerializer(serializers.ModelSerializer):
    """
    Handles the serialization of the Tariff model while adding a custom method for
    generating the payment URL.

    The TariffSerializer class is responsible for taking data from the Tariff model
    and converting it to a format suitable for rendering or transfer, such as JSON.
    It includes a custom field, `payment_url`, which builds a URL for payments
    based on the tariff price and a predefined label. This class provides an easy
    mechanism for serializing both standard fields and calculated fields.

    Attributes:
        payment_url (SerializerMethodField): A dynamically generated field for
        producing a payment URL based on the instance data.

    Methods:
        get_payment_url(self, obj): Constructs and returns the payment URL for a
        given Tariff instance.
    """
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Tariff
        fields = ['id', 'name', 'price', 'duration', 'payment_url']

    def get_payment_url(self, obj):
        return f"https://pay.yandex.ru/to/410012736276443?sum={obj.price}&label=123456789"


# class UserTariffSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='tariff.id')
#     name = serializers.CharField(source='tariff.name')
#     price = serializers.IntegerField(source='tariff.price')
#     duration = serializers.IntegerField(source='tariff.duration')
#
#
#     class Meta:
#         model = UserTariff
#         fields = ['id', 'name', 'price', 'duration', 'start_date', 'end_date']
