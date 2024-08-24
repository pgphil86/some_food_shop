from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . models import Cart, CartItem, Category, Product
from .serializers import (CartSerializer,
                          CartItemSerializer,
                          CategorySerializer,
                          ProductSerializer
                          )


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request, *args, **kwargs):
        cart = self. get_cart(request.user)
        serializer = CartItemSerializer(cart)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request, *args, **kwargs):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartSerializer(cart).data)

    def delete_cart(self, request):
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
