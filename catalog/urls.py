from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView, ContactInfListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, UserProductListView, CategoryProductListView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:category_pk>', CategoryProductListView.as_view(), name='product_category'),
    path('contacts/', cache_page(100_000)(ContactInfListView.as_view()), name='contacts'),
    path('product/<int:pk>/version/<int:version_pk>/', cache_page(10_000)(ProductDetailView.as_view()), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('myproducts/', UserProductListView.as_view(), name='myproducts')
]
