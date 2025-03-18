from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import random
from datetime import date
from rest_framework import viewsets
from .models import User, Contacts, filials,AdressUser,Adresses_of_users
from .serializers import UserSerializer, ContactsSerializer, FilialsSerializer,AdressUserSerializer,AdressesOfUsersSerializer
import json
from rest_framework import generics, permissions
from .utils import generate_otp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
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

    return JsonResponse({'error': 'Invalid request method..'}, status=405)


User = get_user_model()

@csrf_exempt
def authenticate_user(request):
    """Foydalanuvchini ro‘yxatdan o‘tkazish yoki tizimga kiritish"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

    phone = data.get('phone')
    code = data.get('code')

    if not phone or not code:
        return JsonResponse({'error': 'Phone and OTP are required.'}, status=400)

    cached_otp = cache.get(phone)
    if not cached_otp or cached_otp != code:
        return JsonResponse({'error': 'Invalid OTP or OTP expired.'}, status=400)

    user = User.objects.filter(phone=phone).first()

    if user:
        # Agar user allaqachon mavjud bo‘lsa, faqat login qilinadi
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'message': 'Login successful.', 'token': str(refresh.access_token)})
    
    # Agar user mavjud bo‘lmasa, ro‘yxatdan o‘tish uchun qo‘shimcha maydonlar tekshiriladi
    name = data.get('name')
    birthdate = data.get('birthdate')

    if not name or not birthdate:
        return JsonResponse({'error': 'Name and birthdate are required for first-time registration.'}, status=400)

    # Yangi foydalanuvchini yaratish
    user = User.objects.create(phone=phone, name=name, birthdate=birthdate)

    refresh = RefreshToken.for_user(user)
    return JsonResponse({'message': 'User registered successfully.', 'token': str(refresh.access_token)})



class AdressUserCreateView(APIView):
    """Foydalanuvchi o'z manzilini qo'shishi uchun API"""
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        data = JSONParser().parse(request)  # JSON ma'lumotlarni o‘qish
        serializer = AdressUserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)  # Foydalanuvchini token orqali olamiz
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)


class AdressUserListView(generics.ListAPIView):
    """Foydalanuvchining barcha manzillarini olish API"""
    serializer_class = AdressUserSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return AdressUser.objects.filter(user=self.request.user)
    

class AdressesOfUsersViewSet(viewsets.ModelViewSet):
    serializer_class = AdressesOfUsersSerializer
    permission_classes = [permissions.IsAuthenticated]  # Faqat login bo'lganlar
    
    def get_queryset(self):
        return Adresses_of_users.objects.filter(user=self.request.user)  # Faqat o‘ziga tegishli
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Contacts Views
class ContactsListCreateView(generics.ListCreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

class ContactsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [permissions.IsAuthenticated]


# Filials Views
class FilialsListCreateView(generics.CreateAPIView):
    queryset = filials.objects.all()
    serializer_class = FilialsSerializer

class FilialsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = filials.objects.all()
    serializer_class = FilialsSerializer
    permission_classes = [permissions.IsAuthenticated]
