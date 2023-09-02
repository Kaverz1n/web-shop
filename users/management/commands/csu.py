from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    '''
    Команда для создания суперюзера
    '''
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@yandex.ru',
            phone='89999999999',
            country='Russian',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('admin')
        user.save()
