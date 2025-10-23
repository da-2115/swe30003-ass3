# in swe30003/urls.py
from django.contrib import admin
from django.urls import path, include
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    # Server-rendered frontend
    path('', inventory_views.index, name='index'),
    path('products/', inventory_views.products_list, name='products_list'),
    path('products/<uuid:pk>/', inventory_views.product_detail, name='product_detail'),
    path('products/new/', inventory_views.ProductCreate.as_view(), name='product_create'),
    path('products/<uuid:pk>/edit/', inventory_views.ProductUpdate.as_view(), name='product_edit'),
    path('products/<uuid:pk>/delete/', inventory_views.ProductDelete.as_view(), name='product_delete'),
    path('inventories/', inventory_views.inventories_list, name='inventories_list'),
    path('inventories/new/', inventory_views.InventoryCreate.as_view(), name='inventory_create'),
    path('inventories/<int:pk>/edit/', inventory_views.InventoryUpdate.as_view(), name='inventory_edit'),
    path('inventories/<int:pk>/delete/', inventory_views.InventoryDelete.as_view(), name='inventory_delete'),
    # Account / customer
    path('register/', inventory_views.register, name='register'),
    path('login/', inventory_views.login_view, name='login'),
    path('logout/', inventory_views.logout_view, name='logout'),
    # Cart and checkout
    path('cart/', inventory_views.view_cart, name='view_cart'),
    path('cart/add/<uuid:product_id>/', inventory_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', inventory_views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', inventory_views.checkout, name='checkout'),
    # Invoice / payment
    path('invoice/<uuid:pk>/', inventory_views.invoice_detail, name='invoice_detail'),
    path('invoice/<uuid:pk>/pay/', inventory_views.pay_invoice, name='pay_invoice'),
    # Reports
    path('reports/', inventory_views.reports_list, name='reports_list'),
    path('reports/<int:pk>/', inventory_views.report_detail, name='report_detail'),
]