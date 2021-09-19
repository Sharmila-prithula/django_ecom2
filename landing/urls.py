from django.urls import path
from .views import (RegisterView, LoginAPIView,LogoutAPIView, 
                    VerifyEmail, RequestPasswordResetEmail, 
                    PasswordTokenCheckAPI, SetNewPasswordAPIView, 
                    BecomeSellerView, SellerCheckAPI, MakeSellerAPIView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/' , VerifyEmail.as_view(), name="verify"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('become-seller/', BecomeSellerView.as_view(),
         name="become-seller"),
    path('become-seller/<uidb64>/<token>/',
         SellerCheckAPI.as_view(), name='become-seller-check'),
    path('make-seller/', MakeSellerAPIView.as_view(),
         name='make-seller'),
]