from django.db import models
import uuid


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return self.username
