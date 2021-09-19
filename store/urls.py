from django.urls import path
from .views import *

urlpatterns = [ 
    path('vendor/',VendorCreate.as_view(), name= 'create-vendor'),
    path('seller/', SellerCreate.as_view(), name= 'create-seller'),
    path('approve-vendor/', ApproveVendorAPIView.as_view(), name= 'approve-vendor')
]