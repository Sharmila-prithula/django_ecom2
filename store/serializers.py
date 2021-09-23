from rest_framework import fields, serializers
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    vendor_owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Vendor
        fields = ('vendor_name', 'vendor_owner','description')

class ApproveVendorSerializer(serializers.Serializer):
    
    active = serializers.BooleanField(default=False)

    class Meta:
        model= Vendor
        fields = ['vendor_id']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= SubCategory
        fields = "__all__"
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField(many = True)
    class Meta:
        model= Category
        fields = "__all__"
    

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Attribute
        fields = "__all__"
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only = True)
    subcategory = serializers.StringRelatedField(read_only = True)
    vendor = serializers.StringRelatedField(read_only = True)
    class Meta:
        model= Product
        fields = "__all__"

    def validate_subcategory(self, category, subcategory):
        if SubCategory.objects.filter(category=category).exists():
            return subcategory
        else:
            raise serializers.ValidationError("sub category not found")