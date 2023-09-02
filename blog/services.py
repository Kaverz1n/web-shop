from catalog.services import send_email


def send_email_100_view(user_email, article_title) -> None:
    '''
    Отправляет e-mail с поздравлением, при достижении
    100 просмотров на статье
    :param user_email: e-mail адрес пользователя
    :param article_title: название статьи
    '''
    title = 'ПОЗДРАВЛЯЕМ!'
    body = f'Ваша статья "{article_title}" достигла 100 просмотров! Удачи и всего наилучшего!'
    send_email(user_email, title, body)
