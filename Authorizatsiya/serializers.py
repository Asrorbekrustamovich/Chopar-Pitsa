from rest_framework import serializers
from .models import User, Contacts, filials,AdressUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'birthdate']

class AdressUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdressUser
        fields = ['id', 'city', 'x_coordinate', 'y_coordinate', 'street', 'house', 'flat']

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'phone', 'email', 'order_number', 'comment', 'text']

class FilialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = filials
        fields = ['id', 'coordinates', 'name', 'city', 'adress', 'phone']