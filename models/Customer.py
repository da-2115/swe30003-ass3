from django.db import models
from .Account import Account


class Customer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
