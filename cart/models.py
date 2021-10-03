from django.db import models
from landing.models import User
from store.models import ProductVariation
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name="cartitem")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productvariation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.user.username) + " " + str(self.productvariation.id)

@receiver(pre_save, sender=CartItem)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product =  ProductVariation.objects.get(id=cart_items.productvariation.id)
    cart_items.price = float(cart_items.quantity) * float(price_of_product.price)
    # total_cart_items = CartItem.objects.filter(user = cart_items.user)
    # cart = Cart.objects.get(id= cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name="order")
    total_price = models.FloatField(default=0)
    total_item = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    #ordereditems = models.ManyToManyField(CartItem, related_name='order')
    # shipping = models.ForeignKey(Shipping, )

    def __str__(self):
        return str(self.user.username)+" "+ str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="orderitem")
    productvariation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.order.user.username)+" order "+ str(self.order.id) + " productvariation "+str(self.productvariation.product.product_name)
