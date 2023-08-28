import json
import os

from django.core.management import BaseCommand

from blog.models import Article
from catalog.models import Category, Product, Version
from users.models import User

JSON_FILE = os.path.abspath('database_data.json')


class Command(BaseCommand):
    '''
    Команда для заполнения данных в базу данных
    с предварительной отчисткой данных
    '''

    def handle(self, *args, **options) -> None:
        Category.objects.all().delete()
        Article.objects.all().delete()

        category_objects = []
        article_objects = []

        with open(JSON_FILE, 'r', encoding='UTF-8') as j_file:
            models_data = json.load(j_file)

        for data in models_data:
            if data['model'] == 'catalog.category':
                category_objects.append(Category(pk=data['pk'], **data['fields']))
        Category.objects.bulk_create(category_objects)

        for data in models_data:
            if data['model'] == 'blog.article':
                article_objects.append(Article(pk=data['pk'], **data['fields']))

        Article.objects.bulk_create(article_objects)
