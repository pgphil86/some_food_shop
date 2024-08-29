# Тестовое задание - "Some food shop".

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)

### Технологии:
1. Django
1. versatileimagefield
1. PyJWT

### Описание:
Some food shop - это проект на Django. В проекте реализованы сущности: продуктов, корзины с продуктами, категорий и подкатегорий продуктов.
У продуктов, категорий и подкатегорий есть свой уникальный слаг. В корзине ведется подсчёт количесвта продуктов и их стоимости.

### Установка

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:pgphil86/some_food_shop.git
```
```
cd some_food_shop
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/bin/activate
```
И установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Затем необходимо сделать миграции:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Запуск сервера:
```
python3 manage.py runserver
```
Есть несколько тестов проекта, можно проверить его на ошибки:
```
pytest
```

### Автор проекта:
Павел Филиппов

[Вверх](https://github.com/pgphil86/some_food_shop?tab=readme-ov-file#тестовое-задание---some-food-shop)

# The test task is "Some food shop".

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)

### Technologies:
1. Django
1. versatileimagefield
1. PyJWT

###  Description:
Some food shop is a Django project. The project implements the following entities: products, baskets of products, categories and subcategories of products.
Products, categories and subcategories have their own unique slug. The number of products and their cost are counted in the basket.

### Installation:

Clone the repository and go to it on the command line:
```
git@github.com:pgphil86/some_food_shop.git
```
```
cd some_food_shop
```
Clone the repository and go to it on the command line:
```
python -m venv venv
```
```
source venv/bin/activate
```
And install the dependencies from the file requirements.txt :
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Then you need to make migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Starting the server:
```
python3 manage.py runserver
```
There are several tests of the project, you can check it for errors:
```
pytest
```

### Author of the project:
Pavel Filippov

[Up](https://github.com/pgphil86/some_food_shop?tab=readme-ov-file#тестовое-задание---some-food-shop)
