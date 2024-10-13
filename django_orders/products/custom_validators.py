# -*- coding: utf-8 -*-
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator


class PositiveDecimalValidator(DecimalValidator):
    """
    Validates that a decimal value is positive and not zero.

    :param value_error: Error message template for invalid values.
    """

    value_error: str = (
        "Невозможно установить цену товара с {} значением. " "Введите значение от 0.01"
    )

    def __call__(self, value: Decimal) -> None:
        """
        Validates the given value for positivity and non-zero.

        :param value: The decimal value to validate.
        """
        super().__call__(value)
        self.check_for_negative(value)
        self.check_for_zero(value)

    def check_for_negative(self, value: Decimal) -> None:
        """
        Checks if the value is negative and raises ValidationError.

        :param value: The decimal value to check.
        """
        if value < Decimal("0"):
            raise ValidationError(self.value_error.format("отрицательным"))

    def check_for_zero(self, value: Decimal) -> None:
        """
        Checks if the value is zero and raises ValidationError.

        :param value: The decimal value to check.
        """
        if value == Decimal("0"):
            raise ValidationError(self.value_error.format("нулевым"))
