import datetime

from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum, F

from products.models import Product


class Order(models.Model):
    """
    Represents an order with products, status, and costs.

    Attributes:
    - total_cost: The total cost of the order.
    - status: The current status of the order.
    - create_dt: The date and time the order was created.
    - confirm_dt: The date and time the order was confirmed.
    """

    STATUS_CHOICES = {
        "PENDING": "Ожидает оплаты",
        "PAID": "Оплачен",
        "CONFIRMED": "Подтвержден",
    }

    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Итоговая сумма"
    )
    status = models.CharField(
        max_length=20, default=STATUS_CHOICES["PENDING"], verbose_name="Статус"
    )
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    payment_dt = models.DateTimeField(
        default=None, null=True, verbose_name="Дата оплаты"
    )
    confirm_dt = models.DateTimeField(
        default=None, null=True, verbose_name="Время подтверждения"
    )

    def __str__(self) -> str:
        return f"Заказ № {self.id} в статусе {self.status}."

    def get_related_products(self) -> QuerySet:
        """
        Retrieves all products related to the current order.

        :return: A QuerySet of order items.
        """
        order_items: QuerySet = self.orderitem.all()
        return order_items

    def update_total_cost(self):
        """
        Updates the total cost of the order by summing the prices
        of the related products and their quantities.

        :return: None
        """
        cost = self.orderitem.annotate(
            price=F("product__price") * F("quantity")
        ).aggregate(total_price=Sum("price"))
        self.total_cost = cost["total_price"] or 0
        self.save()

    def update_payment_status(self) -> None:
        """
        Updates the status of the order to 'Paid' after payment.

        :return: None
        """
        self.status = self.STATUS_CHOICES["PAID"]
        self.save()

    def update_confirmation_status(self) -> None:
        """
        Updates the status of the order to 'Confirmed'
        after confirmation.

        :return: None
        """
        if self.payment_dt and self.status != self.STATUS_CHOICES["CONFIRMED"]:
            self.status = self.STATUS_CHOICES["CONFIRMED"]
            self.save()

    def update_payment_date(self):
        self.payment_dt = datetime.datetime.now(tz=datetime.timezone.utc)
        self.save()

    def update_confirm_date(self):
        self.confirm_dt = datetime.datetime.now(tz=datetime.timezone.utc)
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    """
    Represents a single item in an order.

    Attributes:
    - order: The related order.
    - product: The product included in the order.
    - quantity: The quantity of the product in the order.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitem")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product"
    )
    quantity = models.PositiveIntegerField(default=1)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        """
        Saves the order item and updates the total cost of the order.

        :param force_insert: Whether to force an insert.
        :param force_update: Whether to force an update.
        :param using: The database to use.
        :param update_fields: Fields to update.
        :return: None
        """
        super().save()
        self.order.update_total_cost()

    def delete(self, *args, **kwargs):
        """
        Deletes the order item and updates the total cost of the order.

        :return: None
        """
        super().delete(*args, **kwargs)
        self.order.update_total_cost()
