from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):
    '''
    Форма для создания и редактирования статьи
    '''
    class Meta:
        model = Article
        fields = ('title', 'body', 'preview', 'is_published',)
