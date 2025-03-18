from rest_framework import serializers
from .models import User, Contacts, filials,AdressUser
from .models import Adresses_of_users

class AdressesOfUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresses_of_users
        fields = '__all__'
        
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