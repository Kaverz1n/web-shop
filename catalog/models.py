from django.db import models

from blog.models import NULLABLE
from users.models import User


# Create your models here.
class Category(models.Model):
    '''
    Модель категории
    '''
    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    '''
    Модель товара
    '''
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='products_images/', verbose_name='Изображение',
                                default='products_images/lg.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.PositiveIntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Дата создания')
    last_change = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ContactInf(models.Model):
    '''
    Модель контактной информации
    '''
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=254, verbose_name='E-mail')
    phone = models.CharField(max_length=10, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return f'{self.fullname} - {self.phone}'

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактные информации'


class Version(models.Model):
    '''
    Модель версии продукта
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.PositiveIntegerField(verbose_name='Номер')
    name = models.CharField(max_length=100, verbose_name='Название')
    is_current = models.BooleanField(verbose_name='Признак текущей версии')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продукта'
