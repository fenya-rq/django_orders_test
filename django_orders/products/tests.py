from decimal import Decimal

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from conftest import _not_existing as nex
from .models import Product
from .custom_validators import PositiveDecimalValidator


@pytest.mark.usefixtures("create_mock_image")
@pytest.mark.django_db
class TestProduct:
    """
    Tests for the Product model.

    Loads the fixtures before start the tests.  Also uses the fixture
    for creating a mock image file as a `Product` field.
    """

    @pytest.fixture(autouse=True)
    def setup_fixtures(self, load_fixture):
        """
        Loads fixtures for the Product model.

        :param load_fixture: The fixture loading function.
        """
        load_fixture("products")

    def test_create_product(self, create_mock_image):
        """
        Tests creating a new product.

        :param create_mock_image: Mock image file for the product.
        """
        product = Product.objects.create(
            name="new_test_product",
            picture=create_mock_image,
            content="new test info",
            price="100.00",
        )
        assert isinstance(product, Product)

    def test_create_product_error(self):
        """
        Tests validation error when creating a product with no picture.
        """
        with pytest.raises(ValidationError):
            Product.objects.create(
                name="new_test_product",
                picture=None,
                content="new test info",
                price="100.00",
            )

    def test_get_product_ok(self):
        """
        Tests validation error when creating a product with no picture.
        """
        product = Product.objects.get(pk=1)
        assert isinstance(product, Product)
        assert str(product) == "Товар test_product стоимостью 200.00."

    def test_get_product_error(self):
        """
        Tests error raised when trying to retrieve a non-existent product.
        """
        with pytest.raises(ObjectDoesNotExist):
            Product.objects.get(pk=nex)

    def test_product_picture_ok(self):
        """
        Tests if the product's picture URL is correct.
        """
        product = Product.objects.get(pk=1)
        assert product.picture.url == r"/media/uploads/2024/10/14/test_image.jpg"

    def test_delete_product_ok(self):
        """
        Tests successful deletion of a product.
        """
        assert Product.objects.get(pk=1).delete()

    def test_delete_product_error(self):
        """
        Tests error raised when deleting a non-existent product.
        """
        with pytest.raises(ObjectDoesNotExist):
            Product.objects.get(pk=nex).delete()


@pytest.mark.parametrize("validator", (PositiveDecimalValidator(10, 2),))
class TestCustomValidator:
    """
    Tests for the custom PositiveDecimalValidator.

    Parametrized with Instance of PositiveDecimalValidator.
    """

    def test_decimal_ok(self, validator):
        """
        Tests that the validator accepts a positive decimal.

        :param validator: Custom decimal validator instance.
        """
        positive_decimal = Decimal("13.64")
        validator(positive_decimal)

    def test_decimal_zero_error(self, validator):
        """
        Tests that the validator raises an error for a zero decimal.

        :param validator: Custom decimal validator instance.
        """
        zero_decimal = Decimal(0)
        with pytest.raises(ValidationError):
            validator(zero_decimal)

    def test_decimal_negative_error(self, validator):
        """
        Tests that the validator raises an error for a negative decimal.

        :param validator: Custom decimal validator instance.
        """
        negative_decimal = Decimal("-13.64")
        with pytest.raises(ValidationError):
            validator(negative_decimal)
