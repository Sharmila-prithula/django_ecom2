from django.db import models
from landing.models import User
# Create your models here.

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=200, unique=True, blank=False)
    vendor_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vendor_name) 

class Seller(models.Model):
    name = models.CharField(max_length=30, blank=False)
    user_seller = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_seller')

    def __str__(self):
        return self.name