from django.db import models
from .Product import Product


class Inventory(models.Model):
    """Inventory grouping of products."""
    name = models.CharField(max_length=200, default='Default Inventory')
    products = models.ManyToManyField(Product, related_name='inventories', blank=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.name} ({self.products.count()} products)"