from rest_framework import serializers

from .models import Cart, CartItem, Category, Product, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'subcategories'
        ]

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return SubcategorySerializer(subcategories, many=True).data


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields =[
            'id',
            'name',
            'slug',
            'image',
            'category'
        ]


class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'subcategory',
            'price',
            'image1',
            'image2',
            'image3'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity'
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items'
        ]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.item.all)
