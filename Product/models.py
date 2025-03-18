from django.db import models
from Authorizatsiya.models import *

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Faqat yaratilganda vaqtni saqlaydi
    updated_at = models.DateTimeField(auto_now=True)  # Har o'zgartirilganda yangilanadi

    class Meta:
        abstract = True


    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField()


    def __str__(self):
        return self.name


class ProductPrice(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField()
    

    def __str__(self):
        return self.name

 
class AdditionalProduct(BaseModel):
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE, related_name="extras")
    image= models.ImageField()
    name=models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

class OrderProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    additionalProduct=models.ForeignKey(AdditionalProduct, on_delete=models.CASCADE,null=True, blank=True)


class Order(BaseModel):
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.ForeignKey(Adress_for_delivery, on_delete=models.CASCADE)
    address_for_take_it=models.ForeignKey(filials, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    products = models.ManyToManyField(OrderProduct, related_name="orders")

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
      