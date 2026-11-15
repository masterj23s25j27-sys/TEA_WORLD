from django.db import models
from django.conf import settings
from products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) # in kg for B2B

    def __str__(self):
        return f"{self.quantity}kg of {self.product.name} in {self.user.username}'s cart"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Payment Received & Preparing'),
        ('SHIPPED', 'In Transit / Logistics dispatch'),
        ('DELIVERED', 'Delivered & Accepted'),
        ('CANCELLED', 'Cancelled'),
    )

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Wallet') # Stripe, PayPal, Razorpay, Wallet
    delivery_address = models.TextField()
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField() # in kg
    price = models.DecimalField(max_digits=10, decimal_places=2) # historical price at time of order

    def __str__(self):
        return f"{self.quantity}kg of {self.product.name if self.product else 'Deleted Product'} at ${self.price}/kg"

    @property
    def total_price(self):
        return self.price * self.quantity
