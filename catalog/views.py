from typing import Any

from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, ContactInf, Version


class ProductListView(ListView):
    '''
    Класс для отображения главной страницы каталога продуктов
    '''
    model = Product

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        last_five_products = Product.objects.order_by('-pk')[:5]
        for product in last_five_products:
            print(f'Товар {product.name} с ценой {product.price}р')

        return context


class ProductDetailView(DetailView):
    '''
    Класс для отображения страницы продукта
    '''
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        version_pk = self.kwargs.get('version_pk')

        if version_pk:
            version = get_object_or_404(Version, pk=version_pk)
            context['version'] = version

        return context


class ProductCreateView(CreateView):
    '''
    Класс для создания нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    '''
    Класс для обновления нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        return self.render_to_response(context)


class ProductDeleteView(DeleteView):
    '''
    Класс для удаления продукта
    '''
    model = Product
    success_url = reverse_lazy('catalog:index')


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
