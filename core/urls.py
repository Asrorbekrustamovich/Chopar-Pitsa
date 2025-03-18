from django.contrib import admin
from django.urls import path, include
from Authorizatsiya.views import *
from Product.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version="v1",
      description="Your API description",
      terms_of_service="https://example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

router = DefaultRouter()
router.register(r'addresses-of-users', AdressesOfUsersViewSet, basename='addresses-of-users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Authorization
    path('api/get-otp/', telefon_raqam_uchun_code_genaratsiya, name='get_otp'),
    path('api/send-otp/', authenticate_user, name='send_otp'),

    # Contacts
    path('api/contacts/', ContactsListCreateView.as_view(), name='contacts-list-create'),
    path('api/contacts/<int:pk>/', ContactsDetailView.as_view(), name='contacts-detail'),

    # Filials
    path('api/filials/', FilialsListCreateView.as_view(), name='filials-list-create'),
    path('api/filials/<int:pk>/', FilialsDetailView.as_view(), name='filials-detail'),

    # Product
    path('product/', ProducListCreateView.as_view()),

    # Orders
    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:pk>/", OrderRetrieveUpdateDeleteView.as_view()),

    # Order Items
    path("order-items/<int:pk>/", OrderItemRetrieveUpdateDeleteView.as_view()),

    # Order Additional Items
    path("order-additional-items/", OrderAdditionalItemListCreateView.as_view()),
    path("order-additional-items/<int:pk>/", OrderAdditionalItemRetrieveUpdateDeleteView.as_view()),

    # Address API
    path('api/address/create/', AdressUserCreateView.as_view(), name='address-create'),
    path('api/address/list/', AdressUserListView.as_view(), name='address-list'),

    # Including router URLs
    path('api/', include(router.urls)),
]
