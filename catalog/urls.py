from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, product, adminka

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>/', product, name='product'),
    path('adminka/', adminka, name='adminka')
]
