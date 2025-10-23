from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    InventoryViewSet,
    AccountViewSet,
    CustomerViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    ReportViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
