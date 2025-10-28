from django.db import models, transaction
from django.core.exceptions import ValidationError
from decimal import Decimal

from .Customer import Customer
from .Product import Product
from .Order import Order, OrderItem

TAX_RATE = Decimal("0.10")  # 10% GST

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "inventory"

    def __str__(self):
        return f"Cart for {self.customer}"

    # ----- totals -----
    def items_qs(self):
        return self.items.select_related("product")

    def subtotal(self) -> Decimal:
        return sum((it.subtotal() for it in self.items_qs()), Decimal("0.00"))

    def tax(self) -> Decimal:
        return (self.subtotal() * TAX_RATE).quantize(Decimal("0.01"))

    def total(self) -> Decimal:
        return (self.subtotal() + self.tax()).quantize(Decimal("0.01"))

    # ----- mutations -----
    @transaction.atomic
    def add_product(self, product: Product, qty: int = 1):
        if qty < 1:
            raise ValidationError("Quantity must be at least 1.")
        if product.stock < qty:
            raise ValidationError(f"Insufficient stock for {product}.")
        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=self, product=product,
            defaults={"quantity": qty, "unit_price": product.price}
        )
        if not created:
            new_qty = item.quantity + qty
            if product.stock < new_qty:
                raise ValidationError(f"Insufficient stock for {product} at quantity {new_qty}.")
            item.quantity = new_qty
        item.unit_price = product.price
        item.full_clean()
        item.save()
        self.save(update_fields=["updated_at"])
        return item

    @transaction.atomic
    def update_item(self, product: Product, qty: int):
        if qty < 1:
            self.remove_product(product)
            return None
        item = CartItem.objects.select_for_update().get(cart=self, product=product)
        if product.stock < qty:
            raise ValidationError(f"Insufficient stock for {product} at quantity {qty}.")
        item.quantity = qty
        item.unit_price = product.price
        item.full_clean()
        item.save()
        self.save(update_fields=["updated_at"])
        return item

    @transaction.atomic
    def remove_product(self, product: Product):
        CartItem.objects.filter(cart=self, product=product).delete()
        self.save(update_fields=["updated_at"])

    @transaction.atomic
    def clear(self):
        self.items.all().delete()
        self.save(update_fields=["updated_at"])

    # ----- checkout -----
    @transaction.atomic
    def checkout_to_order(self) -> Order:
        items = list(self.items_qs().select_for_update())
        if not items:
            raise ValidationError("Cart is empty.")
        # stock check
        for it in items:
            if it.product.stock < it.quantity:
                raise ValidationError(f"Insufficient stock for {it.product}.")
        order = Order.objects.create(customer=self.customer)
        total = Decimal("0.00")
        for it in items:
            it.product.stock -= it.quantity
            it.product.save(update_fields=["stock"])
            OrderItem.objects.create(
                order=order,
                product=it.product,
                quantity=it.quantity,
                unit_price=it.unit_price,
            )
            total += it.unit_price * it.quantity
        order.total = total.quantize(Decimal("0.01"))
        order.save(update_fields=["total"])
        self.clear()
        return order


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = "inventory"
        unique_together = ("cart", "product")

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")

    def subtotal(self) -> Decimal:
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.quantity} × {self.product} @ {self.unit_price}"
