from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView, ContactInfListView, ProductDetailView, ProductCreateView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', ContactInfListView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('admin_panel/', ProductCreateView.as_view(), name='admin_panel')
]
