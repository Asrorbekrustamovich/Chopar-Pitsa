from rest_framework import serializers
from .models import User, City, Delivery_type, Adress_for_delivery, Contacts, filials

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'birthdate']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_type
        fields = ['id', 'name']

class AddressForDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Adress_for_delivery
        fields = ['id', 'city', 'street', 'house', 'flat']

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'phone', 'email', 'order_number', 'comment', 'text']

class FilialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = filials
        fields = ['id', 'coordinates', 'name', 'city', 'adress', 'phone']