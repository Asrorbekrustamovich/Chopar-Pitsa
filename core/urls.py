
from django.contrib import admin
from django.urls import path
from Authorizatsiya.views import *
from Product.views import *

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

    
    # Product urls
      # Orders
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderRetrieveUpdateDeleteView.as_view(), name="order-detail"),

    # Order Items
    path("order-items/", OrderItemListCreateView.as_view(), name="order-item-list-create"),
    path("order-items/<int:pk>/", OrderItemRetrieveUpdateDeleteView.as_view(), name="order-item-detail"),

    # Order Additional Items
    path("order-additional-items/", OrderAdditionalItemListCreateView.as_view(), name="order-additional-item-list-create"),
    path("order-additional-items/<int:pk>/", OrderAdditionalItemRetrieveUpdateDeleteView.as_view(), name="order-additional-item-detail"),

    
]
