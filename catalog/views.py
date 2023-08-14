from typing import Any

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product, ContactInf


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


class ProductCreateView(CreateView):
    '''
    Класс для создания нового продукта в интернет-магазине
    '''
    model = Product
    fields = ('name', 'description', 'preview', 'category', 'price')
    success_url = reverse_lazy('catalog:index')


class ContactInfListView(ListView):
    '''
    Класс для отображения страницы контактов
    '''
    model = ContactInf
    extra_context = {'title': 'Контакты'}

    def post(self, request):
        if request.method == 'POST':
            data = {}
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            data['user_1'] = (name, email, message)
            print(data)

        return redirect('catalog:contacts')
