from django.db import models
from Authorizatsiya.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        abstract = True


    def __str__(self):
        return self.name

class Banner(BaseModel):
    image = models.ImageField()


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


class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order #{self.id} - {self.user.username if self.user else 'Guest'}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_price.product.name} ({self.product_price.size}cm)"


class OrderAdditionalItem(BaseModel):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="additional_items")
    additional_product = models.ForeignKey(AdditionalProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.additional_product.name} for {self.order_item.product_price.product.name}"