from typing import Any

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, ContactInf, Version
from catalog.services import get_categories, get_category_by_pk
from users.models import User


class ProductListView(ListView):
    '''
    Класс для отображения главной страницы каталога продуктов
    '''
    model = Product

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = get_categories()

        return context


class CategoryProductListView(ProductListView):
    '''
    Класс для отображения продуктов на главной странице по категориям
    '''

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        queryset = super().get_queryset(*args, **kwargs)
        category = get_category_by_pk(self.kwargs.get('category_pk'))
        queryset = queryset.filter(category=category)

        return queryset


class ProductDetailView(DetailView):
    '''
    Класс для отображения страницы продукта
    '''
    model = Product

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        version_pk = self.kwargs.get('version_pk')

        if version_pk:
            version = get_object_or_404(Version, pk=version_pk)
            context['version'] = version

        context['title'] = f'Продукт {self.object.name}'

        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    Класс для создания нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:myproducts')

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Созданние продукта'
        return context


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    Класс для обновления нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'

    def __get_user_and_group(self) -> (User, Group):
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

        return user, group

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        user, group = self.__get_user_and_group()

        if self.get_object().user.pk != user.pk and not group:
            return redirect('catalog:index')
        elif group and self.get_object().is_published:
            return redirect('catalog:index')

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self) -> forms:
        user, group = self.__get_user_and_group()

        if group:
            return ModeratorProductForm
        return self.form_class

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)

        context['title'] = f'Редактирование продукта {self.object.name}'

        return context

    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()
        formset = context['formset']
        user, group = self.__get_user_and_group()

        if form.is_valid() and group:
            form.save()
            return super().form_valid(form)

        if form.is_valid() and formset.is_valid():
            if user.pk == self.object.user.pk:
                self.object = form.save()
                self.object.is_published = False
                self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        return self.render_to_response(context)

    def get_success_url(self) -> str:
        user, group = self.__get_user_and_group()

        if group:
            return reverse('catalog:index')

        return reverse('catalog:myproducts')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    Класс для удаления продукта
    '''
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

        if self.get_object().user.pk != user.pk and not group:
            return redirect('catalog:index')
        elif group and self.get_object().is_published:
            return redirect('catalog:index')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта {self.object.name}'
        return context


class ContactInfListView(ListView):
    '''
    Класс для отображения страницы контактов
    '''
    model = ContactInf
    extra_context = {'title': 'Контакты'}

    def post(self, request) -> HttpResponse:
        if request.method == 'POST':
            data = {}
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            data['user_1'] = (name, email, message)
            print(data)

        return redirect('catalog:contacts')

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контактная информация'
        return context


class UserProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    '''
    Класс для отображения продуктов, созданных пользователем
    '''
    model = Product
    permission_required = 'catalog.check_products'
    template_name = 'catalog/product_user.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset
