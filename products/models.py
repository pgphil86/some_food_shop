from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField, PPOIField


class Category(models.Model):
    """
    Модель категории продуктов.
    """
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True, max_length=25)
    image = models.ImageField(upload_to='img/categories/', blank=False)

    def save(self, *args, **kwargs):
        """
        Переопределяет метод сохранения для
        автоматической генерации слага подкатегории,
        если он не был указан.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Модель подкатегории продукта.
    """
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True, max_length=25)
    image = models.ImageField(upload_to='img/subcategories/', blank=False)
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        """
        Переопределяет метод сохранения для
        автоматической генерации слага подкатегории,
        если он не был указан.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продуктов.
    """
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True, max_length=25)
    image = VersatileImageField(
        'Image',
        upload_to='img/products/',
        ppoi_field='ppoi',
        blank=True
    )
    ppoi = PPOIField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(
        Subcategory,
        related_name='products',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        """
        Переопределяет метод сохранения для
        автоматической генерации слага подкатегории,
        если он не был указан.
        """
        self.clean()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        """
        Очищает данные продукта перед сохранением, проверяя,
        является ли цена положительным числом
        и не превышает ли она допустимый лимит.
        """
        if self.price is None or self.price <= 0:
            raise ValidationError('Цена должна быть положительным числом.')
        if self.price > 9999999.99:
            raise ValidationError('Цена слишком велика.')

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Модель корзины.
    """
    user = models.ForeignKey(
        User,
        models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    def total_price(self):
        """
        Рассчитывает общую стоимость продуктов в корзине.
        """
        return self.quantity * self.product.price

    def __str__(self):
        return f'Корзина {self.user.username} {self.product.name}'
