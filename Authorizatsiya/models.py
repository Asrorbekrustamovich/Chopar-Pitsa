from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'birthdate']

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Delivery_type(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Adress_for_delivery(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    flat = models.CharField(max_length=100)
    def __str__(self):
        return self.street+" "+self.house+" "+self.flat

class Contacts(models.Model):
    name = models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    order_number=models.CharField(max_length=100)
    comment=models.TextField()
    text = models.TextField()
    def __str__(self):
        return self.name
class filials(models.Model):
    coordinates = models.PointField()
    name=models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    adress = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    def __str__(self):
        return self.adress

