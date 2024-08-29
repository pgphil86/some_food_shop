import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from products.models import Category, Cart, Product, Subcategory


@pytest.mark.django_db
def test_category_slug_generation():
    """
    Тест на создание слага категории.
    """
    category = Category.objects.create(name='Test Category')
    assert category.slug == 'test-category'


@pytest.mark.django_db
def test_subcategory_slug_generation():
    """
    Тест на создание слага подкатегории.
    """
    category = Category.objects.create(name='Test Category')
    subcategory = Subcategory.objects.create(name='Test Subcategory',
                                             category=category)
    assert subcategory.slug == 'test-subcategory'


@pytest.mark.django_db
def test_product_slug_generation():
    """
    Тест на создание слага продукта.
    """
    category = Category.objects.create(name='Test Category')
    subcategory = Subcategory.objects.create(name='Test Subcategory',
                                             category=category)
    product = Product.objects.create(name='Test Product', price=10.00,
                                     subcategory=subcategory)
    assert product.slug == 'test-product'


@pytest.mark.django_db
def test_product_price_validation():
    """
    Валидация цены продукта (Отрицательная и превышающая предел).
    """
    category = Category.objects.create(name='Test Category')
    subcategory = Subcategory.objects.create(name='Test Subcategory',
                                             category=category)
    with pytest.raises(ValidationError):
        product = Product(name='Test Product', price=-10.00,
                          subcategory=subcategory)
        product.clean()
    with pytest.raises(ValidationError):
        product = Product(name='Test Product', price=10000000.00,
                          subcategory=subcategory)
        product.clean()


@pytest.mark.django_db
def test_cart_total_price():
    """
    Тест проверяет корректность вычисления
    общей суммы стоимости продуктов в корзине.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Test Category')
    subcategory = Subcategory.objects.create(name='Test Subcategory',
                                             category=category)
    product = Product.objects.create(name='Test Product', price=10.00,
                                     subcategory=subcategory)
    cart_item = Cart.objects.create(user=user, product=product, quantity=3)
    assert cart_item.total_price() == 30.00


@pytest.mark.django_db
def test_cart_str_representation():
    """
    Тестирует строковое представление объекта корзины.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    category = Category.objects.create(name='Test Category')
    subcategory = Subcategory.objects.create(name='Test Subcategory',
                                             category=category)
    product = Product.objects.create(name='Test Product', price=10.00,
                                     subcategory=subcategory)
    cart_item = Cart.objects.create(user=user, product=product, quantity=1)
    assert str(cart_item) == f'Корзина {user.username} {product.name}'
