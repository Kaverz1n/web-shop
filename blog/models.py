from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='Slug', **NULLABLE)
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', default='blog/blog_deffault.jpg', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_counter = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
