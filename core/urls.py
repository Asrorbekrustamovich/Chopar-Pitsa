
from django.contrib import admin
from django.urls import path
from Authorizatsiya.views import *
from Product.views import *

urlpatterns = [
     path('admin/', admin.site.urls),

    path('api/filials/', FilialsListCreateView.as_view(), name='filials-list-create'),
    path('api/filials/<int:pk>/', FilialsDetailView.as_view(), name='filials-detail'),

    
    # Product urls
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
    path("api/adresses_of_user/",AdressesOfUsersViewSet.as_view(),name="adresses_of_user"),

    # Including router URLs
    path('api/', include(router.urls)),
]
