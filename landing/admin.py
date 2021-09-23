from django.contrib import admin
from landing.models import User
from store.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Attribute)
admin.site.register(Product)