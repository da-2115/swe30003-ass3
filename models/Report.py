from django.db import models
from django.db.models import Sum, F  # (Count can be used via models.Count)
from decimal import Decimal


class Report(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        app_label = "inventory"

    def __str__(self):
        return self.name

    def generate_sales_overview(self, date_from=None, date_to=None):
        # Local import to avoid circulars
        from .Order import Order, OrderItem

        qs = Order.objects.all()
        if date_from:
            qs = qs.filter(created_at__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__lte=date_to)

        totals = qs.aggregate(
            orders_count=models.Count("id"),
            revenue=Sum("total"),
        )
        items = OrderItem.objects.filter(order__in=qs).aggregate(
            items_sold=Sum("quantity"),
            gross=Sum(F("unit_price") * F("quantity")),
        )

        summary = {
            "orders": totals.get("orders_count") or 0,
            "revenue": str((totals.get("revenue") or Decimal("0.00")).quantize(Decimal("0.01"))),
            "items_sold": items.get("items_sold") or 0,
            "gross": str((items.get("gross") or Decimal("0.00")).quantize(Decimal("0.01"))),
            "filters": {
                "from": str(date_from) if date_from else None,
                "to": str(date_to) if date_to else None,
            },
        }
        self.data = summary
        self.save(update_fields=["data"])
        return summary
