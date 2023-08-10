from django.contrib import admin

from catalog.models import Category, Product, ContactInf


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    ordering = ('pk',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('pk',)


@admin.register(ContactInf)
class ContactInfAdmib(admin.ModelAdmin):
    list_display = ('pk', 'fullname', 'email', 'phone', 'address')
    ordering = ('pk',)
