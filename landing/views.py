#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .serializers import (RegisterSerializer, SetNewPasswordSerializer, 
                            ResetPasswordEmailRequestSerializer, 
                            LoginSerializer, LogoutSerializer, EmailVerificationSerializer,
                            BecomeSellerSerializer, MakeSellerSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
#import jwt
import uuid
from django.conf import settings
from django.contrib import messages
#from drf_yasg.utils import swagger_auto_schema
#from drf_yasg import openapi
#from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
#from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data= request.data)
            
            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            #email_verification_token = str(uuid.uuid4())
            account = serializer.save()
            #email = request.POST.get('email')
            user = User.objects.get(email = account.email)
            user.email_verification_token = str(uuid.uuid4())
            user.save()
            send_mail_after_registration(request.data['email'] , user.email_verification_token)
            return Response({'status' : 200, 'messsage' : 'an otp sent on your mail'})

        except Exception as e:
            print(e)

            return Response({'status' : 404, 'errors' :'something went wrong'})

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, token):
        try:
            serializer = self.serializer_class(data= request.data)
            email_verification_token = token
        
            user = User.objects.get(email_verification_token = email_verification_token)
            if user.is_verified:
                return Response({'email': 'already activated'}, status=status.HTTP_200_OK)
            user.is_verified = True
            user.save()
            #return user
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status' : 404, 'errors' :'something went wrong'})

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://localhost:8000/landing/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def send_mail_to_reset_password(email , token):
    subject = 'Your password reset link'
    message = f'Hi paste the link to reset your password http://localhost:8000/landing/password-reset/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        user = User.objects.get(email = email)
        if user.is_verified:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status' : 404, 'errors' :'verify your email'})

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            tokenid = uidb64 + "/" + token
            send_mail_to_reset_password(request.data['email'] , tokenid)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'status' : 404, 'errors' :'Token is not valid. Request another one.'})                    
            return Response({'status' : 200, 'message' :'Token valid','uidb64':uidb64 })
            

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'status' : 404, 'errors' :'Token is not valid. Request another one.'})                    

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class BecomeSellerView(generics.GenericAPIView):
    serializer_class = BecomeSellerSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            adm = User.objects.get(is_staff=True)
            emailAdmin = adm.email
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            tokenid = uidb64 + "/" + token
            subject = 'Make this user a seller'
            message = f'Hi paste the link to make this account seller http://localhost:8000/landing/become-seller/{tokenid}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [emailAdmin]
            send_mail(subject, message , email_from ,recipient_list )
            return Response({'success': 'Wait for the admin approval'}, status=status.HTTP_200_OK)

class SellerCheckAPI(generics.GenericAPIView):
    #permissions_classes= (permissions.IsAuthenticated,)
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'status' : 404, 'errors' :'Token is not valid. Request another one.'})                    
            return Response({'status' : 200, 'message' :'Token valid','uidb64':uidb64, 'email':user.email})

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'status' : 404, 'errors' :'Token is not valid. Request another one.'})                    

class MakeSellerAPIView(generics.GenericAPIView):
    serializer_class = MakeSellerSerializer
    permission_classes = (permissions.IsAdminUser,)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully changed this user seller status'}, status=status.HTTP_200_OK)
