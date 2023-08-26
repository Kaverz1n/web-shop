from catalog.utils import send_email


def send_email_100_view(user_email, article_title):
    '''
    Отправляет e-mail с поздравлением, при достижении
    100 просмотров на статье
    '''
    title = 'ПОЗДРАВЛЯЕМ!'
    body = f'Ваша статья "{article_title}" достигла 100 просмотров! Удачи и всего наилучшего!'
    send_email(user_email, title, body)
