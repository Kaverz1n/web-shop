# Generated by Django 4.2.3 on 2023-08-11 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_contactinf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='preview',
            field=models.ImageField(default='products_images/lg.jpg', upload_to='products_images/', verbose_name='Изображение'),
        ),
    ]
