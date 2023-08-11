from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, ContactInf, Category


def index(request) -> HttpResponse:
    '''
    Контролер для главной страницы интернет-магазина
    :return: HTTP-ответ с отображением шаблона "index.html"
    '''
    last_five_products = Product.objects.order_by('-pk')[:5]
    for product in last_five_products:
        print(f'Товар {product.name} с ценой {product.price}р')

    products_list = Product.objects.all()

    context = {
        'object_list': products_list,
        'title': 'Главная страница'
    }

    return render(request, 'catalog/index.html', context)


def contacts(request) -> HttpResponse:
    '''
    Контролер для страницы контакты интернет-магазина
    :return: HTTP-ответ с отображением шаблона "contacts.html"
    '''
    if request.method == 'POST':
        data = {}
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        data['user_1'] = (name, email, message)
        print(data)

    inf_list = ContactInf.objects.all()

    context = {
        'object_list': inf_list,
        'title': 'Контакты'
    }

    return render(request, 'catalog/contacts.html', context)


def product(request, pk) -> HttpResponse:
    '''
    Контролер для страницы товара интернет-магазина
    :return: HTTP-ответ с отображением шаблона "product.html"
    '''
    product = get_object_or_404(Product, id=pk)
    return render(request, 'catalog/product.html', {'object': product})


def admin_panel(request) -> HttpResponse:
    '''
    Контролер для страницы админа интернет-магазина
    :return: HTTP-ответ с отображением шаблона "product.html"
    '''
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = int(request.POST.get('price'))
            category_id = int(request.POST.get('category'))
            category = Category.objects.get(pk=category_id)
            product_inf = {'name': name, 'description': description, 'price': price}

            Product.objects.create(category=category, **product_inf)
        except ValueError:
            pass

    return render(request, 'catalog/admin_panel.html')
