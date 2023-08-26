import os

from django.core.mail import send_mail

from shop.settings import EMAIL_HOST_USER


def get_wrong_words():
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


def send_email(user_email, title, body):
    '''
    Отправляет e-mail пользователю
    '''
    admin_email = EMAIL_HOST_USER

    try:
        send_mail(title, body, admin_email, [user_email])
    except:
        print('ОШИБКА ОТПРАВКИ')
