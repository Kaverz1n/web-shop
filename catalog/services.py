import os

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from catalog.models import Category


def get_wrong_words() -> list[str]:
    '''
    Возвращает список слов, которые не должны быть использованы
    в названии или описании продукта.
    :return: список неверных слов
    '''
    FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wrong_words.txt')

    with open(FILE_PATH, 'r', encoding='UTF-8') as file:
        data = file.read()
        wrong_words = data.split(',')

    return wrong_words


def send_email(user_email, title, body) -> None:
    '''
    Отправляет e-mail пользователю
    :param user_email: e-mail пользователя
    :param title: имя сообщения
    :param body: тело сообщения
    '''
    admin_email = settings.EMAIL_HOST_USER

    try:
        send_mail(title, body, admin_email, [user_email])
    except:
        print('ОШИБКА ОТПРАВКИ')


def get_categories() -> list[Category]:
    '''
    Возвращает все категории магазина, предварительно
    проверив их в кэше
    :return: список объектов Category
    '''
    if settings.CACHE_ENABLED:
        cache_key = 'categories'
        categories_list = cache.get(cache_key)
        if categories_list is None:
            categories = Category.objects.all()
            categories_list = cache.set(cache_key, categories, 10_000)
    else:
        categories_list = Category.objects.all()

    return categories_list


def get_category_by_pk(category_pk) -> Category:
    '''
    Возвращает категорию магазина по переданному первичному ключу
    :param category_pk: первичный ключ категории
    :return: объект Category
    '''
    categories_list = get_categories()

    for object in categories_list:
        if object.pk == category_pk:
            category = get_object_or_404(Category, pk=object.id)

    return category
