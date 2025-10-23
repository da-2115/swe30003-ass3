from django.db import models


class Report(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return self.name
