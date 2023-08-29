from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from pytils.translit import slugify

from blog.models import Article
from blog.utils import send_email_100_view


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        return context


class ArticleDetailView(DetailView):
    '''
    Класс для отображения выбраной статьи
    '''
    model = Article

    def get_object(self, queryset=None) -> Article:
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()

        if self.object.views_counter == 100:
            send_email_100_view('email@yandex.ru', self.object.title)

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статья {self.object.title}'
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи'
        return context


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование статьи {self.object.title}'
        return context


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Класс для отображения страницы удаления статьи
    '''
    model = Article
    success_url = reverse_lazy('blog:view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи {self.object.title}'
        return context
