from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import random
from datetime import date
from rest_framework import viewsets
from .models import User, City, Delivery_type, Adress_for_delivery, Contacts, filials
from .serializers import UserSerializer, CitySerializer, DeliveryTypeSerializer, AddressForDeliverySerializer, ContactsSerializer, FilialsSerializer
import json
from rest_framework import generics, permissions
from .utils import generate_otp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import permissions

@csrf_exempt
def telefon_raqam_uchun_code_genaratsiya(request):
    """Telefon raqam bo‘yicha OTP kod yaratish va cache'ga saqlash"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON dan ma'lumotlarni olish
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

        phone = data.get('phone')

        if not phone:
            return JsonResponse({'error': 'Phone number is required.'}, status=400)

        otp = generate_otp()  # Yangi OTP yaratish
        cache.set(phone, otp, timeout=120)  # OTP ni cache'ga 2 daqiqa saqlash
        print(f"Generated OTP for {phone}: {otp}")  # Konsolga chiqarish

        return JsonResponse({'otp': otp, 'message': 'OTP generated and cached successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def registratsiya(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON ma'lumotlarni o‘qish
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

        phone = data.get('phone')
        name = data.get('name')
        birthdate = data.get('birthdate')
        code = data.get('code')  # Foydalanuvchi kiritgan OTP

        if not phone:
            return JsonResponse({'error': 'Phone number is required.'}, status=400)

        is_first_time = not User.objects.filter(phone=phone).exists()

        if is_first_time and (not name or not birthdate):
            return JsonResponse({'error': 'Name and birthdate are required for first-time registration.'}, status=400)

        cached_otp = cache.get(phone)  # Cache'dan OTP ni olish
        if not cached_otp:
            return JsonResponse({'error': 'OTP expired or not found. Please request a new one.'}, status=400)

        if code != cached_otp:
            return JsonResponse({'error': 'Invalid OTP. Please try again.'}, status=400)

        # Agar foydalanuvchi avval ro‘yxatdan o‘tgan bo‘lsa
        user = User.objects.filter(phone=phone).first()
        if user:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return JsonResponse({'message': 'OTP verified successfully.', 'token': token})

        # Agar foydalanuvchi yangi bo‘lsa, uni yaratamiz
        user = User.objects.create(
            phone=phone,
            name=name,
            birthdate=birthdate
        )
        user.set_password(code)  # OTP ni vaqtinchalik parol sifatida saqlash
        user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return JsonResponse({'message': 'User registered successfully.', 'token': token})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login(request):
    """Telefon raqami va OTP orqali foydalanuvchini tekshirish va token qaytarish"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON formatda kelgan ma'lumotlarni o‘qish
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

        phone = data.get('phone')
        otp_entered = data.get('otp')

        if not phone or not otp_entered:
            return JsonResponse({'error': 'Phone and OTP are required.'}, status=400)

        otp_cached = cache.get(phone)  # Cache'dan OTP ni olish

        if otp_cached and otp_cached == otp_entered:
            user = User.objects.filter(phone=phone).first()  # Foydalanuvchini topish

            if not user:
                return JsonResponse({'error': 'User not found.'}, status=404)

            # Token yaratish
            refresh = RefreshToken.for_user(user)  
            token = str(refresh.access_token)

            return JsonResponse({'message': 'Login successful.', 'token': token})

        return JsonResponse({'error': 'Invalid OTP or OTP expired.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication


# Delivery Type Views
class DeliveryTypeListCreateView(generics.ListCreateAPIView):
    queryset = Delivery_type.objects.all()
    serializer_class = DeliveryTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delivery_type.objects.all()
    serializer_class = DeliveryTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


# Address for Delivery Views
class AddressForDeliveryListCreateView(generics.ListCreateAPIView):
    queryset = Adress_for_delivery.objects.all()
    serializer_class = AddressForDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

class AddressForDeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Adress_for_delivery.objects.all()
    serializer_class = AddressForDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]


# Contacts Views
class ContactsListCreateView(generics.ListCreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [permissions.IsAuthenticated]


# Filials Views
class FilialsListCreateView(generics.ListCreateAPIView):
    queryset = filials.objects.all()
    serializer_class = FilialsSerializer
    permission_classes = [permissions.IsAuthenticated]

class FilialsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = filials.objects.all()
    serializer_class = FilialsSerializer
    permission_classes = [permissions.IsAuthenticated]

