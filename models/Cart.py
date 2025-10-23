from django.db import models
from .Product import Product
from .Customer import Customer


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"Cart for {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'inventory'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product}"
