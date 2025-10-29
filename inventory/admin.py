from django.contrib import admin
from .models.Cart import Cart, CartItem
from .models.Order import Order, OrderItem
from .models.Report import Report


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'updated_at', 'cart_total')
    search_fields = ('customer__name',)
    list_filter = ('updated_at',)
    readonly_fields = ('cart_total',)

    def cart_total(self, obj):
        # uses Cart.total() you already implemented
        try:
            return f"${obj.total():.2f}"
        except Exception:
            return "-"
    cart_total.short_description = "Cart Total ($)"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price', 'item_subtotal')
    list_filter = ('product',)
    search_fields = ('product__name',)
    readonly_fields = ('item_subtotal',)

    def item_subtotal(self, obj):
        return f"${obj.subtotal():.2f}"
    item_subtotal.short_description = "Subtotal ($)"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'total')
    search_fields = ('id', 'customer__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'line_total')
    search_fields = ('product__name', 'order__id')
    readonly_fields = ('line_total',)

    def line_total(self, obj):
        # uses OrderItem.line_total() you added
        return f"${obj.line_total():.2f}"
    line_total.short_description = "Line Total ($)"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('data',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'
