import re
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import viewsets
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, views, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from landing.models import User
from .serializers import *
from .permissions import *
import uuid
# Create your views here.
class VendorCreate(generics.CreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Review.objects.all()

    def perform_create(self, serializer):
        vendor_owner = self.request.user
        vendor = serializer.save(vendor_owner=vendor_owner)
        adm = User.objects.get(is_staff=True)
        emailAdmin = adm.email
        subject = 'Make this vendor active'
        vendor_id = vendor.id
        message = f'Hi paste the link to make this vendor active http://localhost:8000/store/approve-vendor/{vendor_id}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [emailAdmin]
        send_mail(subject, message , email_from ,recipient_list )
        return Response({'success': 'created vendor. wait for admin approve'}, status=status.HTTP_200_OK)

class ApproveVendorAPIView(generics.GenericAPIView):
    serializer_class = ApproveVendorSerializer
    permission_classes = (permissions.IsAdminUser,)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        id = request.data.get('vendor_id', '')
        active = request.data.get('active', '')
        if Vendor.objects.filter(id=id).exists():
            vendor = Vendor.objects.get(id=id)
            vendor.active = active
            vendor.save()
            serializer.is_valid(raise_exception=True)
            
            return Response({'success': True, 'message': 'Successfully changed this active status', 'name':vendor.vendor_name, 'status':vendor.active}, status=status.HTTP_200_OK)
        return Response({'status' : 404, 'errors' :'something went wrong'}) 

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        category= Category.objects.all()
        return category


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        category = SubCategory.objects.all()
        return category

    def create(self, request, *args, **kwargs):
        data = request.data 
        
        category_obj = Category.objects.get(id=data["category"])
        
        subcategory = SubCategory.objects.create(
            subcategory_name=data["subcategory_name"], category=category_obj)

        subcategory.save()
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data=request.data
        instance = self.get_object()
        serializer = self.serializer_class(instance, data)
        serializer.is_valid(raise_exception=True)

        #subcategory = SubCategory.objects.get(id=id)
        instance.subcategory_name = data["subcategory_name"]
        instance.description = data["description"]
        instance.category= Category.objects.get(id=data["category"])
        
        instance.save()

        serializer = SubCategorySerializer(instance)

        return Response(serializer.data)


class AttributeViewSet(viewsets.ModelViewSet):
    serializer_class = AttributeSerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        category = Attribute.objects.all()
        return category

    def create(self, request, *args, **kwargs):
        data = request.data 
        attribute = Attribute.objects.create(
            attribute_name=data["attribute_name"])

        attribute.save()
        for subcategory in data["subcategories"]:
            subcategory_obj = SubCategory.objects.get(id=subcategory["id"])
            attribute.subcategories.add(subcategory_obj)
        
        serializer = AttributeSerializer(attribute)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data=request.data
        instance = self.get_object()
        serializer = self.serializer_class(instance, data)
        serializer.is_valid(raise_exception=True)

        #attribute = attribute.objects.get(id=id)
        instance.attribute_name = data["attribute_name"]
        for subcategory in data["subcategories"]:
            subcategory_obj = SubCategory.objects.get(id=subcategory["id"])
            instance.subcategories.add(subcategory_obj)
        
        instance.save()

        serializer = AttributeSerializer(instance)

        return Response(serializer.data)

class ProductView(APIView):
    permission_classes = [IsOwner]
    def get(self, request, pk):
        product = Product.objects.filter(vendor=pk)
        serializer = ProductSerializer(product, many=True) 
        return Response(serializer.data)

    def post(self, request, pk):
        data=request.data
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        category = Category.objects.get(id=data["category"])
        subcategory = SubCategory.objects.get(id=data["subcategory"])
        product = Product.objects.create(product_name=data["product_name"], description=data["description"], category=category, subcategory=subcategory, vendor=obj)
        for attribute in data["attributes"]:
            attribute_obj = Attribute.objects.get(id=attribute)
            product.attributes.add(attribute_obj)
        for variant in data["variants"]:
            variant_obj = Variant.objects.get(id=variant)
            product.variants.add(variant_obj)
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [IsOwner]
    
    def get(self, request, pk, prok):
        
        product = Product.objects.get(id=prok)
        serializer = ProductSerializer(product) 
        return Response(serializer.data)

    def put(self, request, pk, prok):
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        data=request.data
        product = Product.objects.get(id=prok)
        category = Category.objects.get(id=data["category"])
        subcategory = SubCategory.objects.get(id=data["subcategory"])
        for attribute in data["attributes"]:
            attribute_obj = Attribute.objects.get(id=attribute)
            product.attributes.add(attribute_obj)
        product.category=category
        product.subcategory=subcategory
        serializer = ProductSerializer(product, data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request,pk, prok):
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        product = Product.objects.get(id=prok)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttributeValueView(APIView):
    permission_classes = [IsOwner]
    def get(self, request,pk, prok, ak):
        attributes = Attribute.objects.filter(product=prok)
        for attribute in attributes:
            if attribute.id==ak:
                attributevalue= AttributeValue.objects.get(attribute=ak)
        serializer = AttributeValueSerializer(attributevalue) 
        return Response(serializer.data)

    def post(self, request, pk, prok, ak):
        data=request.data
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        product = Product.objects.get(id=prok)
        attribute = Attribute.objects.get(id=ak)
        attributevalue = AttributeValue.objects.create(attributevalue_name=data["attributevalue_name"], product=product, attribute=attribute)
        attributevalue.save()
        serializer = AttributeValueSerializer(attributevalue)
        return Response(serializer.data)

class AttributeValueDetailView(APIView):
    permission_classes = [IsOwner]
    
    def get(self, request, pk, prok, ak, avk):
        
        attributevalue = AttributeValue.objects.get(id=avk)
        serializer = AttributeValueSerializer(attributevalue) 
        return Response(serializer.data)

    def put(self, request, pk, prok, ak, avk):
        data=request.data
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        attributevalue = AttributeValue.objects.get(id=avk)
        product = Product.objects.get(id=prok)
        attribute = Attribute.objects.get(id=ak)
        attributevalue.product = product
        attributevalue.attribute = attribute
        serializer = AttributeValueSerializer(attributevalue, data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request,pk,ak, prok, avk):
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        attributevalue = AttributeValue.objects.get(id=avk)
        attributevalue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VariantView(APIView):
    def get(self, request):
        variant = Variant.objects.all() 
        serializer = VariantSerializer(variant, many=True) 
        return Response(serializer.data)
    

class OptionView(APIView):
    def get(self, request, pk):
        option = Option.objects.filter(variant=pk) 
        serializer = OptionSerializer(option, many=True) 
        return Response(serializer.data)

class ProductVariationView(APIView):
    permission_classes = [IsOwner]
    def get(self, request, pk, prok):
        productvariation = ProductVariation.objects.filter(product=prok)
        serializer = ProductVariationSerializer(productvariation, many=True) 
        return Response(serializer.data)

    def post(self, request, pk, prok):
        data=request.data
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        product = Product.objects.get(id=prok)
        productvariation = ProductVariation.objects.create(price=data["price"], stock=data["stock"], image=data["image"], product=product)
        for variant in data["variants"]:
            variant_obj = Variant.objects.get(id=variant)
            productvariation.variants.add(variant_obj)
        for option in data["options"]:
            option_obj = Option.objects.get(id=option)
            productvariation.options.add(option_obj)
        productvariation.save()
        serializer = ProductVariationSerializer(productvariation)
        return Response(serializer.data)

class ProductVariationDetailView(APIView):
    permission_classes = [IsOwner]
    
    def get(self, request, pk, prok, pvk):
        
        productvariation = ProductVariation.objects.get(id=pvk)
        serializer = ProductVariationSerializer(productvariation) 
        return Response(serializer.data)

    def put(self, request, pk, prok, pvk):
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        data=request.data
        productvariation = ProductVariation.objects.get(id=pvk)
        product = Product.objects.get(id=prok)       
        for variant in data["variants"]:
            variant_obj = Variant.objects.get(id=variant)
            productvariation.variants.add(variant_obj)
        
        for option in data["options"]:
            option_obj = Option.objects.get(id=option)
            productvariation.options.add(option_obj)
        productvariation.product = product
        serializer = ProductVariationSerializer(productvariation, data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request,pk, prok, pvk):
        obj = Vendor.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        productvariation = ProductVariation.objects.get(id=pvk)
        productvariation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
