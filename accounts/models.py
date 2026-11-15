from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('BUYER', 'Buyer / Client'),
        ('VENDOR', 'Tea Vendor / Estate Owner'),
        ('DISTRIBUTOR', 'Distributor / Wholesaler'),
        ('DELIVERY', 'Delivery & Logistics Partner'),
        ('ADMIN', 'Platform Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='BUYER')
    phone = models.CharField(max_length=15, blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00) # seeded with $100k for wholesale trade simulation
    company_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def is_buyer(self):
        return self.role == 'BUYER'

    def is_vendor(self):
        return self.role == 'VENDOR'

    def is_distributor(self):
        return self.role == 'DISTRIBUTOR'

    def is_delivery(self):
        return self.role == 'DELIVERY'

    def is_platform_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
