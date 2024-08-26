from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . models import Cart, Category, Product, Subcategory
from .pagination import PagePagination
from .serializers import (CartSerializer,
                          CategorySerializer,
                          ProductSerializer,
                          SubcategorySerializer
                          )


class CategoryListView(generics.ListAPIView):
    """
    Вью для категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PagePagination


class SubcategoryListView(generics.ListAPIView):
    """
    Вью для подкатегорий.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    pagination_class = PagePagination


class ProductListView(generics.ListAPIView):
    """
    Вью для продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PagePagination


class CartView(views.APIView):
    """
    Вью для корзины.
    Только для аутентифицированного пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        return Cart.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user,
                                                        product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartSerializer(cart_item).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        Cart.objects.filter(user=request.user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartSerializer(cart_item).data)
