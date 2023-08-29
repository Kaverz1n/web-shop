from django import template

register = template.Library()


@register.filter
def mediapath(url) -> str:
    '''
    Кастомный тег, который выстраивает путь
    к файлам, которые содержатся в папке media
    '''
    result = f"/media/{url}"
    return result


@register.simple_tag
def mediapath(url) -> str:
    '''
    Кастомный тег, который выстраивает путь
    к файлам, которые содержатся в папке media
    '''
    result = f"/media/{url}"
    return result


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
