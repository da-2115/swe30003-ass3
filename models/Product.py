from django.db import models
import uuid


class Product(models.Model):
    """Product model for SWE30003 inventory app.

    Fields:
    - id: UUID primary key
    - name: product name
    - description: optional long description
    - price: decimal price
    - stock: integer stock quantity
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return self.name