from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status, views
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']
    ordering_fields = ['name']


class SubcategoryListView(generics.ListAPIView):
    """
    Вью для подкатегорий.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'category']
    ordering_fields = ['name', 'category']


class ProductListView(generics.ListAPIView):
    """
    Вью для продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'subcategory', 'price']
    ordering_fields = ['name', 'price']


class CartView(views.APIView):
    """
    Вью для работы с корзиной.
    Только для аутентифицированного пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        return Cart.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        """
        Вывод состава корзины с подсчетом количества товаров и общей стоимости.
        """
        cart_items = self.get_cart(request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_cost = sum(item.total_price() for item in cart_items)
        data = {
            'items': CartSerializer(cart_items, many=True).data,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        Добавление продукта в корзину.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = Cart.objects.get_or_create(user=request.user,
                                                            product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()
            return Response(CartSerializer(cart_item).data,
                            status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        Изменение количества продукта в корзине.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        try:
            cart_item = Cart.objects.get(user=request.user,
                                         product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                return Response(CartSerializer(cart_item).data)
            else:
                return Response({'error': 'Quantity must be greater than 0'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        Удаление продукта из корзины.
        """
        product_id = request.data.get('product_id')
        try:
            cart_item = Cart.objects.get(user=request.user,
                                         product_id=product_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'},
                            status=status.HTTP_404_NOT_FOUND)
