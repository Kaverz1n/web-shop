import json
import os

from django.core.management import BaseCommand
from catalog.models import Category, Product, Version

JSON_FILE = os.path.abspath('database_data.json')


class Command(BaseCommand):
    '''
    Команда для заполнения данных в базу данных
    с предварительной отчисткой данных
    '''

    def handle(self, *args, **options) -> None:
        Category.objects.all().delete()
        Product.objects.all().delete()
        Version.objects.all().delete()

        category_objects = []
        product_objects = []
        version_objects = []

        with open(JSON_FILE, 'r', encoding='UTF-8') as j_file:
            models_data = json.load(j_file)

        for data in models_data:
            if data['model'] == 'catalog.category':
                category_objects.append(Category(pk=data['pk'], **data['fields']))
        Category.objects.bulk_create(category_objects)

        for data in models_data:
            if data['model'] == 'catalog.product':
                category_id = data['fields'].pop('category')
                category = Category.objects.get(pk=category_id)
                product_objects.append(Product(pk=data['pk'], category=category, **data['fields']))
        Product.objects.bulk_create(product_objects)

        for data in models_data:
            if data['model'] == 'catalog.version':
                product_id = data['fields'].pop('product')
                product = Product.objects.get(pk=product_id)
                version_objects.append(Version(pk=data['pk'], product=product, **data['fields']))

        Version.objects.bulk_create(version_objects)
