from django.db import models
from django.conf import settings
from apps.products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Delivery Info
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # ✅ ADD THESE
    quantity_kg = models.IntegerField(null=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity_kg}kg)"