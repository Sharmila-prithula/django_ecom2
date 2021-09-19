from django.contrib import admin
from landing.models import User
from store.models import Vendor, Seller
# Register your models here.
admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Seller)