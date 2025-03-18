from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone, name, birthdate, password=None, **extra_fields):
        """Oddiy foydalanuvchi yaratish uchun funksiya"""
        if not phone:
            raise ValueError('The Phone field must be set')

        user = self.model(phone=phone, name=name, birthdate=birthdate, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        """Superuser yaratish uchun funksiya"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, name, birthdate="2000-01-01", password=password, **extra_fields)  # birthdate default beriladi

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_permission_set",
        blank=True
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

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
    coordinates = models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    adress = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    def __str__(self):
        return self.adress

