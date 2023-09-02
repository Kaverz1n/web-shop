from django.contrib import admin

from catalog.models import Category, Product, ContactInf, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    ordering = ('pk',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category', 'is_published',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)
    ordering = ('pk',)


@admin.register(ContactInf)
class ContactInfAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fullname', 'email', 'phone', 'address',)
    ordering = ('pk',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'number', 'name', 'is_current',)
    ordering = ('pk',)
    list_filter = ('product', 'is_current',)
