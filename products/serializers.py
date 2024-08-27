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
        """
        Возвращает сериализованные данные всех подкатегорий.
        """
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
    category = serializers.CharField(source='subcategory.category.name',
                                     read_only=True)
    subcategory = serializers.CharField(source='subcategory.name',
                                        read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'subcategory',
            'price',
            'images'
        ]

    def get_images(self, obj):
        """
        Возвращает словарь с URL-адресами
        изображений продукта в разных размерах.
        """
        return {
            'small': obj.image.thumbnail['small'].url if obj.image else None,
            'medium': obj.image.thumbnail['medium'].url if obj.image else None,
            'large': obj.image.thumbnail['large'].url if obj.image else None,
        }


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор корзины.
    """
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'product',
            'quantity',
            'total_price'
        ]
