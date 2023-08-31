from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
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

        context['title'] = f'Продукт {self.object.name}'

        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    Класс для создания нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Созданние продукта'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Класс для обновления нового продукта в интернет-магазине
    '''
    model = Product
    form_class = ProductForm

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

        if self.get_object().user.pk != user.pk and not group:
            return redirect('catalog:index')
        elif group and self.get_object().is_published:
            return redirect('catalog:index')

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        user = self.request.user
        group = user.groups.filter(name='product_moderator')
        if group:
            return ModeratorProductForm
        return self.form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)

        context['title'] = f'Редактирование продукта {self.object.name}'

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

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

    def get_success_url(self):
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

        if group:
            return reverse('catalog:index')

        return reverse('catalog:myproducts')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Класс для удаления продукта
    '''
    model = Product
    success_url = reverse_lazy('catalog:index')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.filter(name='product_moderator')

        if self.get_object().user.pk != user.pk and not group:
            return redirect('catalog:index')
        elif group and self.get_object().is_published:
            return redirect('catalog:index')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контактная информация'
        return context


class UserProductListView(PermissionRequiredMixin, ListView):
    model = Product
    permission_required = 'catalog.check_products'
    template_name = 'catalog/product_user.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset
