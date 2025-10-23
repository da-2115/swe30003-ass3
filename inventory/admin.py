from django.contrib import admin
from .models import Product, Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('products',)
