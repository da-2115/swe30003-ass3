from django.db import models
from .Customer import Customer
from .Product import Product
import uuid


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"Order {self.id} ({self.customer})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.quantity} x {self.product} @ {self.unit_price}"
