from django.db import models

from . import PositiveDecimalValidator


class Product(models.Model):
    """
    Represents a product with associated attributes.

    Attributes:
    - name: The name of the product.
    - picture: The image associated with the product.
    - image_width: The width of the product image.
    - image_height: The height of the product image.
    - content: Description of the product.
    - price: The price of the product.
    """

    name = models.CharField(max_length=40, verbose_name="Название")
    picture = models.ImageField(
        verbose_name="Изображение",
        upload_to="uploads/%Y/%m/%d/",
        width_field="image_width",
        height_field="image_height",
    )
    image_width = models.PositiveIntegerField(verbose_name="Ширина", editable=False)
    image_height = models.PositiveIntegerField(verbose_name="Высота", editable=False)
    content = models.TextField(max_length=600, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        validators=[PositiveDecimalValidator(max_digits=10, decimal_places=2)],
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        """
        Returns a string representation of the product.

        :return: A formatted string showing the product name and price.
        """
        return f"Товар {self.name} стоимостью {self.price}."

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        """
        Saves the product instance after validation.

        Validates the model before saving it to the database.

        :param args: Additional positional arguments.
        :param force_insert: Whether to force an insert.
        :param force_update: Whether to force an update.
        :param using: The database to use.
        :param update_fields: The fields to update.
        """
        self.full_clean()
        super().save()
