from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Order, OrderItem, OrderAdditionalItem, Product
from .serializers import OrderSerializer, OrderItemSerializer, OrderAdditionalItemSerializer,ProductSerializer


class ProducListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]



class OrderListCreateView(generics.ListCreateAPIView):
   
   # Buyurtmalarni ko'rish va yaratish API
   
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin barcha buyurtmalarni ko'radi, oddiy foydalanuvchi faqat o'z buyurtmalarini ko'radi
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # Yangi buyurtma yaratishda foydalanuvchini qo'shish
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
  
    # Bitta buyurtmani ko'rish, tahrirlash yoki o'chirish
   
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderItemListCreateView(generics.ListCreateAPIView):
  
    # Buyurtmaga mahsulot qo'shish va ko'rish API
 
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin barcha buyurtma mahsulotlarini ko'rishi mumkin, oddiy user faqat o'z buyurtmalarini ko'radi
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)


class OrderItemRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    
    # Bitta buyurtma mahsulotini ko'rish, tahrirlash yoki o'chirish
    
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderAdditionalItemListCreateView(generics.ListCreateAPIView):
    
    # Buyurtmaga qo'shimcha mahsulot qo'shish va ko'rish API
    
    queryset = OrderAdditionalItem.objects.all()
    serializer_class = OrderAdditionalItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin barcha qo'shimcha mahsulotlarni ko'rishi mumkin, oddiy user faqat o'z buyurtmalariga tegishlilarini ko'radi
        user = self.request.user
        if user.is_staff:
            return OrderAdditionalItem.objects.all()
        return OrderAdditionalItem.objects.filter(order_item__order__user=user)


class OrderAdditionalItemRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    
    # Bitta qo'shimcha mahsulotni ko'rish, tahrirlash yoki o'chirish
    
    queryset = OrderAdditionalItem.objects.all()
    serializer_class = OrderAdditionalItemSerializer
    permission_classes = [permissions.IsAuthenticated]
