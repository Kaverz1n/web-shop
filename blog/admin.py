from django.contrib import admin

from blog.models import Article


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'is_published', 'views_counter')
    list_filter = ('is_published',)
    search_fields = ('title', 'body')
    ordering = ('pk',)
