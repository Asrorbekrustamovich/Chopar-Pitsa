from rest_framework import serializers
from .models import Order, OrderItem, OrderAdditionalItem, ProductPrice, AdditionalProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'description']


class ProductPriceSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  

    class Meta:
        model = ProductPrice
        fields = ['id', 'product', 'price', 'size']


class AdditionalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProduct
        fields = ['id', 'name', 'image', 'price']


class OrderAdditionalItemSerializer(serializers.ModelSerializer):
    additional_product = AdditionalProductSerializer(read_only=True)  

    class Meta:
        model = OrderAdditionalItem
        fields = ['id', 'additional_product', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product_price = ProductPriceSerializer(read_only=True)  
    additional_items = OrderAdditionalItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_price', 'quantity', 'additional_items']

    def validate_quantity(self, value):
        """Buyurtma mahsulotining miqdori 1 dan kam bo'lmasligi kerak"""
        if value < 1:
            raise serializers.ValidationError("Mahsulot miqdori kamida 1 bo'lishi kerak.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    items = OrderItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'items']
