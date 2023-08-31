# Generated by Django 4.2.3 on 2023-08-28 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published', 'Can publish products'), ('change_description', 'Can change product description'), ('change_category', 'Can change product category')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
