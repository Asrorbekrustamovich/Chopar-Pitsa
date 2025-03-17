"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Authorizatsiya.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/get-otp/', telefon_raqam_uchun_code_genaratsiya, name='get_otp'),
    path('api/send-otp/', registratsiya, name='send_otp'),  # OTP yuborish endpointi
    path('api/verify-otp/', login, name='verify_otp'),
     path('api/cities/', CityListCreateView.as_view(), name='city-list-create'),
    path('api/cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),

    # Delivery Type
    path('api/delivery-types/', DeliveryTypeListCreateView.as_view(), name='delivery-type-list-create'),
    path('api/delivery-types/<int:pk>/', DeliveryTypeDetailView.as_view(), name='delivery-type-detail'),

    # Address for Delivery
    path('api/addresses/', AddressForDeliveryListCreateView.as_view(), name='address-list-create'),
    path('api/addresses/<int:pk>/', AddressForDeliveryDetailView.as_view(), name='address-detail'),

    # Contacts
    path('api/contacts/', ContactsListCreateView.as_view(), name='contacts-list-create'),
    path('api/contacts/<int:pk>/', ContactsDetailView.as_view(), name='contacts-detail'),

    # Filials
    path('api/filials/', FilialsListCreateView.as_view(), name='filials-list-create'),
    path('api/filials/<int:pk>/', FilialsDetailView.as_view(), name='filials-detail'),
]
