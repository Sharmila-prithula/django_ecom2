from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("attributes", AttributeViewSet, basename="attribute")
router.register("categories", CategoryViewSet, basename="categories")
router.register("subcategories", SubCategoryViewSet, basename="subcategories")

urlpatterns = [ 
    path('', include(router.urls)),
    path('vendor/',VendorCreate.as_view(), name= 'create-vendor'),
    path('approve-vendor/', ApproveVendorAPIView.as_view(), name= 'approve-vendor'),
    # path('subcategories/', SubCategoryView.as_view(), name= 'subcategories'),
    # path('subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name= 'subcategories-detail'),
]