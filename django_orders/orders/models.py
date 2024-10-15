from django.db import models
from django.db.models import Sum, F

from products.models import Product


class OrderStatus(models.Model):
    status = models.CharField(max_length=15, verbose_name="Статус заказа")

    def __str__(self) -> str:
        return f"ID: {self.id}, Статус: {self.status}"

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ("id",)


class Order(models.Model):
    PENDING = "pending"
    PAID = "paid"
    CONFIRMED = "confirmed"

    STATUS_CHOICES = [
        (PENDING, "Ожидает оплаты"),
        (PAID, "Оплачен"),
        (CONFIRMED, "Подтвержден"),
    ]

    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Итоговая сумма"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING, verbose_name="Статус"
    )
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    confirm_dt = models.DateTimeField(
        default=None, null=True, verbose_name="Время подтверждения"
    )

    def __str__(self) -> str:
        return f"Заказ {self.id} в статусе {self.status}."

    def get_related_products(self) -> list:
        order_items = self.orderitem.all()
        return order_items

    def update_total_cost(self):
        cost = self.orderitem.annotate(
            price=F("product__price") * F("quantity")
        ).aggregate(total_price=Sum("price"))
        self.total_cost = cost["total_price"] or 0
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitem")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    quantity = models.PositiveIntegerField(default=1)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        super().save()
        self.order.update_total_cost()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total_cost()
