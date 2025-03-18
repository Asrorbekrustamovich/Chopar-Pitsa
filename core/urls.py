
from django.contrib import admin
from django.urls import path
from Authorizatsiya.views import *
from Product.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/get-otp/', telefon_raqam_uchun_code_genaratsiya, name='get_otp'),
    path('api/send-otp/',authenticate_user , name='send_otp'),

    # Contacts
    path('api/contacts/', ContactsListCreateView.as_view(), name='contacts-list-create'),
    path('api/contacts/<int:pk>/', ContactsDetailView.as_view(), name='contacts-detail'),

    # Filials
    path('api/filials/', FilialsListCreateView.as_view(), name='filials-list-create'),
    path('api/filials/<int:pk>/', FilialsDetailView.as_view(), name='filials-detail'),

    
    # Product urls
    path('product/', ProducListCreateView.as_view()),
      # Orders
    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:pk>/", OrderRetrieveUpdateDeleteView.as_view()),

    # Order Items
    path("order-items/", OrderItemListCreateView.as_view()),
    path("order-items/<int:pk>/", OrderItemRetrieveUpdateDeleteView.as_view()),

    # Order Additional Items
    path("order-additional-items/", OrderAdditionalItemListCreateView.as_view()),
    path("order-additional-items/<int:pk>/", OrderAdditionalItemRetrieveUpdateDeleteView.as_view()),

    
]
