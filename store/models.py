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

class Variant(models.Model):
    variant_name = models.CharField(max_length=200, unique=True, blank=False)
    subcategories = models.ManyToManyField(SubCategory, related_name="variant")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.variant_name)

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, blank=False)
    description = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="product")
    attributes = models.ManyToManyField(Attribute, related_name="product")
    variants = models.ManyToManyField(Variant, related_name="product")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="product")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product_name)

class Option(models.Model):
    option_name = models.CharField(max_length=200, unique=True, blank=False)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="option")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.option_name)

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productvariation")
    variants = models.ManyToManyField(Variant, related_name="productvariation")
    options = models.ManyToManyField(Option, related_name="productvariation")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class AttributeValue(models.Model):
    attributevalue_name = models.CharField(max_length=200, unique=True, blank=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="attributevalue")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributevalue")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.attributevalue_name)