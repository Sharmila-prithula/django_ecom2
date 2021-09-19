from django.shortcuts import render
from rest_framework import generics
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, views, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from landing.models import User
from .serializers import *
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
        
class SellerCreate(APIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        serializer = SellerSerializer(data=request.data)
        if user.is_seller:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status' : 404, 'errors' :'User is not approved for seller.'})

        

