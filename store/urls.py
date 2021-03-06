from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("attributes", AttributeViewSet, basename="attribute")
router.register("categories", CategoryViewSet, basename="categories")
router.register("subcategories", SubCategoryViewSet, basename="subcategories")
router.register("products", ProductViewSet, basename="product")
#router.register("<int:pk>/products", ProductViewSet, basename="products")

urlpatterns = [ 
    path('', include(router.urls)),
    path('vendorcreate/',VendorCreate.as_view(), name= 'create-vendor'),
    path('vendors/',VendorView.as_view(), name= 'vendors'),
    path('vendors/<int:pk>/',VendorDetailView.as_view(), name= 'vendor-detail'),
    path('approve-vendor/', ApproveVendorAPIView.as_view(), name= 'approve-vendor'),
    path('variants/',VariantView.as_view(), name= 'variant'),
    path('<int:pk>/options/',OptionView.as_view(), name= 'option'),
    path('<int:pk>/products/', ProductView.as_view(), name='products'),
    path('product/', ProductList.as_view(), name='product'),
    path('<int:pk>/products/<int:prok>/', ProductDetailView.as_view(), name='products-details'),
    path('products/<int:prok>/', ProductDetailLandingView.as_view(), name='landing-products-details'),
    path('products/<int:prok>/productvariations/', ProductVariationLandingView.as_view(), name='landing-products-variation'),
    path('products/<int:prok>/productvariations/<int:pvk>/', ProductVariationDetailLandingView.as_view(), name='landing-products-variation-detail'),
    path('<int:pk>/products/<int:prok>/<int:ak>/attributevalues/', AttributeValueView.as_view(), name='attributevalue'),
    path('<int:pk>/products/<int:prok>/<int:ak>/attributevalues/<int:avk>/', AttributeValueDetailView.as_view(), name='attributevalue-detail'),
    path('<int:pk>/products/<int:prok>/productvariations/', ProductVariationView.as_view(), name='products-variation'),
    path('<int:pk>/products/<int:prok>/productvariations/<int:pvk>/', ProductVariationDetailView.as_view(), name='products-variation-detail'),
]