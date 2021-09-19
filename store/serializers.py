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
    
class SellerSerializer(serializers.ModelSerializer):
    vendor =  VendorSerializer(many=True, read_only=True)

    class Meta:
        model = Seller
        fields = "__all__"