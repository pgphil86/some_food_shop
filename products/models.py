from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Модель категории продуктов.
    """
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='img/categories/')

    def save(self, *args, **kwargs):
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
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='img/subcategories/')
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
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
    slug = models.SlugField(unique=True)
    image1 = models.ImageField(upload_to='img/products/')
    image2 = models.ImageField(upload_to='img/products/')
    image3 = models.ImageField(upload_to='img/products/')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    subcategory = models.ForeignKey(
        Subcategory,
        related_name='products',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

    def __str__(self):
        return f'Корзина {self.user.username} {self.product.name}'

    def total_price(self):
        return self.quantity * self.product.price
