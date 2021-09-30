from rest_framework import serializers
from .models import *
from store.serializers import *

class CartItemSerializer(serializers.ModelSerializer):
    #cart = CartSerializer()
    productvariation = ProductVariationSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cartitem = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = Cart
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    #cart = CartSerializer()
    orderitem = serializers.StringRelatedField(many = True)
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    #order = OrderSerializer()
    productvariation = serializers.StringRelatedField(many = True)

    class Meta:
        model = OrderItem
        fields = '__all__'