# Generated by Django 5.1 on 2024-08-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_image1_remove_product_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='img/categories/'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(upload_to='img/subcategories/'),
        ),
    ]
