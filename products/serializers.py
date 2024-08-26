from rest_framework import serializers

from .models import Cart, Category, Product, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории.
    """
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
    """
    Сериализатор подкатегории.
    """

    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'category'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор продукта.
    """
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


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины.
    """
    items = ProductSerializer()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'product',
            'quantity',
            'total_price'
        ]
