from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

class CartView(APIView):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request):
        data=request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user=user)
        productvariation = ProductVariation.objects.get(id=data.get('productvariation'))
        price = productvariation.price
        quantity = data.get('quantity')

        cart_item = CartItem(user=user, productvariation=productvariation,cart=cart, quantity=quantity, price=price)
        cart_item.save()

        total_price = 0
        cart_items = CartItem.objects.filter(user=user, cart=cart.id)
        for item in cart_items:
            total_price += item.price
        cart.ordered = False
        cart.total_price = total_price
        cart.save()

        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data)

    # def put(self, request):
    #     user = request.user
    #     data = request.data
    #     cart = Cart.objects.filter(user=user, ordered=False).first()

    #     cart_item = CartItem.objects.get(id=data.get('id'))
    #     #cart.total_price = cart.total_price-cart_item.price
    #     #cart.save()
    #     quan = data.get('quantity')
    #     quantity = int(quan)
    #     id= cart_item.productvariation.id
    #     productvariation = ProductVariation.objects.get(id=id)
    #     cart_item.quantity += quantity
    #     # print (float(productvariation.price) * float(quantity))
    #     # print(cart.total_price)
    #     # if quantity>0:
    #     #     cart.total_price += float(productvariation.price) * float(quantity)
    #     # elif quantity<0:
    #     cart.total_price += float(productvariation.price) * float(quantity)
    #     #cart.total_price += cart_item.price
    #     cart_item.save()
    #     cart.save()
    #     queryset = CartItem.objects.filter(cart=cart)
    #     serializer = CartItemSerializer(queryset, many = True)
    #     return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data
        cart = Cart.objects.filter(user=user, ordered=False).first()

        cart_item = CartItem.objects.get(id=data.get('id'))
        quan = data.get('quantity')
        quantity = int(quan)
        id= cart_item.productvariation.id
        productvariation = ProductVariation.objects.get(id=id)
        cart_item.quantity += quantity
        if cart_item.quantity < 0:
            return Response({'status' : 404, 'errors' :'item cannot be negative'}) 
        cart.total_price += float(productvariation.price) * float(quantity)
        cart_item.save()
        cart.save()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        data = request.data
        cart = Cart.objects.filter(user=user, ordered=False).first()

        cart_item = CartItem.objects.get(id=data.get('id'))
        cart.total_price -= cart_item.price
        cart_item.delete()
        cart.save()

        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data)

class OrderView(APIView):
    def get(self, request):
        user = request.user
        # queryset = Order.objects.filter(user=user)
        # serializer = OrderSerializer(queryset, many=True) 
        # return Response(serializer.data)
        order = Order.objects.filter(user=user).first()
        queryset = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(user=user, cart=cart, total_price=cart.total_price)
        cartitems = CartItem.objects.filter(user=user, cart=cart)
        for cartitem in cartitems:
            productvariation= ProductVariation.objects.get(id=cartitem.productvariation.id)
            productvariation.stock -= cartitem.quantity
            if productvariation.stock < 0:
                return Response({'status' : 404, 'errors' :productvariation.product.product_name +' is sold out'}) 
            productvariation.save()
            order.total_item = order.total_item + 1
            orderitem= OrderItem.objects.create(order=order, productvariation=productvariation, quantity=cartitem.quantity, price=cartitem.price)
        order.save()
        for cartitem in cartitems:
            cartitem.delete() 
        cart.ordered = True
        cart.total_price = 0
        cart.save()
        
        #order = Order.objects.filter(user=user).first()
        queryset = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(queryset, many = True)
        return Response(serializer.data)
