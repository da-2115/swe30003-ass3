from django.contrib import admin
from .models import Product, Inventory
from .models.Cart import Cart, CartItem
from .models.Order import Order, OrderItem
from .models.Report import Report

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('products',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'updated_at',)
    search_fields = ('customer__name',)
    list_filter = ('updated_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price')
    list_filter = ('product',)
    search_fields = ('product__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'total')
    search_fields = ('id', 'customer__name')
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price')
    search_fields = ('product__name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('data',)
