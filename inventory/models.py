"""Re-export models from the project's top-level `models` package.

This ensures the Django `inventory` app uses the model definitions located in
`/Users/dylan/Source/SWE30003/models/` (Product.py and Inventory.py).
"""
try:
    # Prefer absolute import from the project's models package
    from models.Product import Product
    from models.Inventory import Inventory
    from models.Account import Account
    from models.Customer import Customer
    from models.Cart import Cart, CartItem
    from models.Order import Order, OrderItem
    from models.Invoice import Invoice, Payment
    from models.Report import Report
except Exception:
    # Fallback: define minimal models to keep the app runnable
    from django.db import models as _models
    import uuid

    class Product(_models.Model):
        id = _models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        name = _models.CharField(max_length=200)
        description = _models.TextField(blank=True)
        price = _models.DecimalField(max_digits=10, decimal_places=2)
        stock = _models.IntegerField(default=0)

        class Meta:
            app_label = 'inventory'

        def __str__(self):
            return self.name

    class Inventory(_models.Model):
        name = _models.CharField(max_length=200, default='Default Inventory')
        products = _models.ManyToManyField(Product, related_name='inventories', blank=True)

        class Meta:
            app_label = 'inventory'

        def __str__(self):
            return self.name
