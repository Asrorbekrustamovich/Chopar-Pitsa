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

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        birthdate = request.POST.get('birthdate')

        # Check if the user is registering for the first time
        is_first_time = not User.objects.filter(phone=phone).exists()

        if is_first_time and (not name or not birthdate):
            return JsonResponse({'error': 'Name and birthdate are required for first-time registration.'}, status=400)

        # Generate OTP
        otp = generate_otp()

        # Store OTP in cache for 2 minutes
        cache.set(phone, otp, timeout=120)  # 120 seconds = 2 minutes

        print(f"OTP for {phone}: {otp}")

        if not is_first_time:
            user = authenticate(phone=phone)
            if user:
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return JsonResponse({
                    'message': 'OTP sent successfully. Check the terminal for the OTP.',
                    'token': token 
                })
            else:
                return JsonResponse({'error': 'User not found.'}, status=404)

        return JsonResponse({'message': 'OTP sent successfully. Check the terminal for the OTP.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def verify_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp_entered = request.POST.get('otp')
        name = request.POST.get('name')
        birthdate = request.POST.get('birthdate')

        # Retrieve OTP from cache
        otp_cached = cache.get(phone)

        if otp_cached and otp_cached == otp_entered:
            # Check if the user is registering for the first time
            is_first_time = not User.objects.filter(phone=phone).exists()

            if is_first_time:
                if not name or not birthdate:
                    return JsonResponse({'error': 'Name and birthdate are required for first-time registration.'}, status=400)

                # Create a new user
                user = User.objects.create_user(
                    phone=phone,
                    name=name,
                    birthdate=birthdate,
                    password=None  # No password required for OTP-based login
                )
                message = 'Registration successful. You are now logged in.'
            else:
                # Authenticate the existing user
                user = authenticate(phone=phone)
                if not user:
                    return JsonResponse({'error': 'User not found.'}, status=404)
                message = 'Login successful.'

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Return token as JSON response
            return JsonResponse({'message': message, 'token': token})
        else:
            return JsonResponse({'error': 'Invalid OTP or OTP expired.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DeliveryTypeViewSet(viewsets.ModelViewSet):
    queryset = Delivery_type.objects.all()
    serializer_class = DeliveryTypeSerializer

class AddressForDeliveryViewSet(viewsets.ModelViewSet):
    queryset = Adress_for_delivery.objects.all()
    serializer_class = AddressForDeliverySerializer

class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

class FilialsViewSet(viewsets.ModelViewSet):
    queryset = filials.objects.all()
    serializer_class = FilialsSerializer