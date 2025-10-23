from django.db import models
from .Order import Order
import uuid


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    issued_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"Invoice {self.id} for {self.order}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default='offline')

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.amount} paid for {self.invoice}"
