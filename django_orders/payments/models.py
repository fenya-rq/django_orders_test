import random
import time

from django.db import models
from django.db.models import ProtectedError
from rest_framework.serializers import ValidationError

from orders.models import Order


class Payment(models.Model):
    """
    Represents a payment for an order.

    Attributes:
    - order: The order related to the payment.
    - cost: The total payment amount.
    - status: The current status of the payment.
    - payment_type: The method used for the payment.
    """

    STATUS_CHOICES = {
        "PENDING": "В процессе",
        "COMPLETED": "Выполнен успешно",
        "FAILED": "Платеж не прошел",
        "VOIDED": "Удален",
    }

    PAYMENT_METHOD_CHOICES = [
        ("Credit Card", "Credit Card"),
        ("PayPal", "PayPal"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payment",
        null=True,
        verbose_name="Заказ",
    )
    cost = models.DecimalField(
        max_digits=25, decimal_places=2, default=0.00, verbose_name="Сумма"
    )
    status = models.CharField(
        max_length=20,
        default=STATUS_CHOICES["PENDING"],
        verbose_name="Статус",
    )
    payment_type = models.CharField(
        max_length=25, choices=PAYMENT_METHOD_CHOICES, verbose_name="Тип оплаты"
    )

    def __str__(self) -> str:
        return f"Платеж с ID {self.id} - {self.status}"

    def void(self):
        self.status = self.STATUS_CHOICES["VOIDED"]

    def get_cost(self) -> None:
        """
        Updates the payment's cost based on the related order's total cost.

        :return: None
        """
        self.cost = self.order.total_cost

    def update_order_status(self) -> None:
        """
        Updates the status of the related order based on payment status.

        If the payment is completed, updates the order's status
        accordingly.
        :return: None
        """
        if self.status == self.STATUS_CHOICES["COMPLETED"]:
            self.order.update_payment_status()

    def update_order_payment_date(self):
        self.order.update_payment_date()

    def imitate_payment_processing(self):
        """
        Simulates payment processing by adding a delay and updating
        the status.

        The status changes from 'pending' to 'completed'
        after processing.
        :return: None
        """
        processing_time = round(random.random(), 2)
        time.sleep(processing_time)
        self.status = self.STATUS_CHOICES["COMPLETED"]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_field=None,
    ) -> None:
        """
        Saves the payment and processes the payment lifecycle.

        - Sets the payment cost based on the order.
        - Simulates payment processing.
        - Updates the related order's status if the payment
          is successful.
        :param force_insert: Whether to force an insert.
        :param force_update: Whether to force an update.
        :param using: The database connection to use.
        :param update_field: Fields to update.
        :return: None
        """
        if self.order.status == self.order.STATUS_CHOICES["PAID"]:
            raise ValidationError("Невозмонжо провести платеж - заказ уже оплачен.")
        if self.status == self.STATUS_CHOICES["VOIDED"]:
            super().save()
            return
        if self.cost == 0:
            self.get_cost()
            self.payment_type = random.choice(self.PAYMENT_METHOD_CHOICES)[1]
            super().save()
        if self.status == self.STATUS_CHOICES["PENDING"]:
            self.imitate_payment_processing()
            super().save()
            self.update_order_status()
            self.update_order_payment_date()

    def delete(self, using=None, keep_parents=False):
        self.void()
        self.save()
        raise ProtectedError(
            f"Payments cannot be deleted. Payment with ID {self.id}: was voided",
            {Payment},
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
