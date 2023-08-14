from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from pytils.translit import slugify

from blog.models import Article


class ArticleListView(ListView):
    '''
    Класс для отображения всех статей блога
    '''
    model = Article
    ordering = ('created_at',)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Article]:
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset


class ArticleDetailView(DetailView):
    '''
    Класс для отображения выбраной статьи
    '''
    model = Article

    def get_object(self, queryset=None) -> Article:
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()

        return self.object


class ArticleCreateView(CreateView):
    '''
    Класс для отображения страницы создания статьи
    '''
    model = Article
    fields = ('title', 'body', 'preview')
    success_url = reverse_lazy('blog:view')

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify('title')
            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    '''
    Класс для отображения страницы обновления статьи
    '''
    model = Article
    fields = ('title', 'body', 'preview')

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)

    def get_success_url(self) -> HttpResponse:
        return reverse('blog:article', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    '''
    Класс для отображения страницы удаления статьи
    '''
    model = Article
    success_url = reverse_lazy('blog:view')
