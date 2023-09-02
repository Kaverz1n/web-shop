from django import template

register = template.Library()


@register.filter
def mediapath(url) -> str:
    '''
    Кастомный тег, который выстраивает путь
    к файлам, которые содержатся в папке media
    :param url: URL-адрес картинки
    :return: полный путь к картинке
    '''
    result = f"/media/{url}"
    return result


@register.simple_tag
def mediapath(url) -> str:
    '''
    Кастомный тег, который выстраивает путь
    к файлам, которые содержатся в папке media
    :param url: URL-адрес картинки
    :return: полный путь к картинке
    '''
    result = f"/media/{url}"
    return result


@register.filter
def has_group(user, group_name) -> bool:
    '''
    Кастомный фильтер, который возвращает True,
    в случае если пользователь относится к определенной
    группе
    :param user: пользователь
    :param group_name: имя группы
    :return: bool-значение
    '''
    return user.groups.filter(name=group_name).exists()
