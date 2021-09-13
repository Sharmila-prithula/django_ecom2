#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
#import jwt
from django.conf import settings
#from drf_yasg.utils import swagger_auto_schema
#from drf_yasg import openapi
#from .renderers import UserRenderer
#from django.contrib.auth.tokens import PasswordResetTokenGenerator
#from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
#from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.contrib.sites.shortcuts import get_current_site
#from django.urls import reverse
#from .utils import Util
#from django.shortcuts import redirect
#from django.http import HttpResponsePermanentRedirect
#import os

# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         account = serializer.save()
#         user_data = {}
#         user_data['response'] = "Registration successful"
#         user_data['username'] = account.username
#         user_data['email'] = account.email

#         #user = User.objects.get(email=user_data['email'])
#         refresh = RefreshToken.for_user(account)
#         #token = RefreshToken.for_user(user).access_token
#         user_data['token'] = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }

#         # current_site = get_current_site(request).domain
#         # relativeLink = reverse('email-verify')
#         # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         # email_body = 'Hi '+user.username + \
#         #     ' Use the link below to verify your email \n' + absurl
#         # data = {'email_body': email_body, 'to_email': user.email,
#         #         'email_subject': 'Verify your email'}
  
#         # Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)

            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.save()
            return Response({'status' : 200, 'messsage' : 'an otp sent on your mail'})

        except Exception as e:
            print(e)

            return Response({'status' : 404, 'errors' :'something went wrong'})

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)