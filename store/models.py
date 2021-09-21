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


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True, blank=False)
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.category_name)


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=200, unique=True, blank=False)
    description = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subcategory_name)

class Attribute(models.Model):
    attribute_name = models.CharField(max_length=200, unique=True, blank=False)
    subcategories = models.ManyToManyField(SubCategory, related_name="attribute")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.attribute_name)

