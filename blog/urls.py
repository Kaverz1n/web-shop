from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView,
    ArticleDeleteView
)

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='view'),
    path('view/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('add/', ArticleCreateView.as_view(), name='create'),
    path('upd/<int:pk>/', ArticleUpdateView.as_view(), name='update'),
    path('del/<int:pk>/', ArticleDeleteView.as_view(), name='delete')
]
