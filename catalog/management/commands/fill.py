import os

from django.core.management import BaseCommand, call_command

JSON_FILE = os.path.abspath('all_database.json')


class Command(BaseCommand):
    '''
    Команда для заполнения данных в базу данных
    с предварительной отчисткой данных
    '''

    def handle(self, *args, **options) -> None:
        try:
            call_command('loaddata', 'all_database.json')
        except:
            pass
