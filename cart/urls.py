from django.urls import path
from .views import *

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('order/', OrderView.as_view(), name='order'),
]
