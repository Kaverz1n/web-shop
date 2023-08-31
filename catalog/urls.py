from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView, ContactInfListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, UserProductListView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', ContactInfListView.as_view(), name='contacts'),
    path('product/<int:pk>/version/<int:version_pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('myproducts/', UserProductListView.as_view(), name='myproducts')
]
