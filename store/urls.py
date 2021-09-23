from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("attributes", AttributeViewSet, basename="attribute")
router.register("categories", CategoryViewSet, basename="categories")
router.register("subcategories", SubCategoryViewSet, basename="subcategories")
#router.register("<int:pk>/products", ProductViewSet, basename="products")

urlpatterns = [ 
    path('', include(router.urls)),
    path('vendor/',VendorCreate.as_view(), name= 'create-vendor'),
    path('approve-vendor/', ApproveVendorAPIView.as_view(), name= 'approve-vendor'),
    path('<int:pk>/variants/',VariantView.as_view(), name= 'variant'),
    path('<int:pk>/options/',OptionView.as_view(), name= 'option'),
    path('<int:pk>/products/', ProductView.as_view(), name='products'),
    path('<int:pk>/products/<int:prok>/', ProductDetailView.as_view(), name='products-details'),
    path('<int:pk>/products/<int:prok>/<int:ak>/attributevalues/', AttributeValueView.as_view(), name='attributevalue'),
    path('<int:pk>/products/<int:prok>/<int:ak>/attributevalues/<int:avk>/', AttributeValueDetailView.as_view(), name='attributevalue-detail'),
    path('<int:pk>/products/<int:prok>/productvariations/', ProductVariationView.as_view(), name='products-variation'),
    path('<int:pk>/products/<int:prok>/productvariations/<int:pvk>/', ProductVariationDetailView.as_view(), name='products-variation-detail'),
]