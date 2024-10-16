import pytest

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError

from conftest import _not_existing as nex
from products.models import Product
from .models import Order, OrderItem


@pytest.mark.django_db
class TestOrderItem:
    @pytest.fixture(autouse=True)
    def setup_method(self, load_fixture):
        """Load required fixtures for OrderItem tests."""
        load_fixture("products")
        load_fixture("orders")
        load_fixture("orderitems")

    def test_get_orderitem_ok(self):
        """Test retrieving an existing OrderItem instance by primary key."""
        order_item: OrderItem = OrderItem.objects.get(pk=1)
        assert isinstance(order_item, OrderItem)

    def test_get_orderitem_error(self):
        """Test retrieving a non-existent OrderItem raises an error."""
        with pytest.raises(ObjectDoesNotExist):
            OrderItem.objects.get(pk=nex)

    def test_create_orderitem_ok(self):
        """Test creating a new OrderItem instance successfully."""
        order: Order = Order.objects.get(pk=1)
        product: Product = Product.objects.get(pk=1)
        order_item: OrderItem = OrderItem.objects.create(
            order=order, product=product, quantity=6
        )
        assert isinstance(order_item, OrderItem)

    def test_create_orderitem_error(self):
        """Test creating OrderItem without required fields raises an error."""
        with pytest.raises(IntegrityError):
            OrderItem.objects.create()

    def test_update_orderitem_ok(self):
        """Test updating an existing OrderItem instance successfully."""
        order_item: OrderItem = OrderItem.objects.get(pk=1)
        product: Product = Product.objects.get(pk=1)
        order_item.product = product
        order_item.save()
        assert order_item.product == product

    def test_update_orderitem_error(self):
        """Test updating OrderItem with invalid data raises a ValueError."""
        order_item: OrderItem = OrderItem.objects.get(pk=1)
        with pytest.raises(ValueError):
            order_item.product = 1

    def test_delete_orderitem_ok(self):
        """Test deleting an existing OrderItem instance successfully."""
        order_item: OrderItem = OrderItem.objects.get(pk=1).delete()
        assert order_item is None

    def test_delete_orderitem_error(self):
        """Test deleting a non-existent OrderItem raises an error."""
        with pytest.raises(ObjectDoesNotExist):
            OrderItem.objects.get(pk=nex).delete()


@pytest.mark.django_db
class TestOrder:
    @pytest.fixture(autouse=True)
    def setup_method(self, load_fixture):
        """Load required fixtures for Order tests."""
        load_fixture("products")
        load_fixture("orders")
        load_fixture("orderitems")

    def test_get_order_ok(self):
        """Test retrieving an existing Order instance by primary key."""
        order_item: Order = Order.objects.get(pk=1)
        assert isinstance(order_item, Order)

    def test_get_order_error(self):
        """Test retrieving a non-existent Order raises an error."""
        with pytest.raises(ObjectDoesNotExist):
            Order.objects.get(pk=nex)

    def test_create_order_ok(self):
        """Test creating a new Order instance successfully."""
        order: Order = Order.objects.create()
        product: Product = Product.objects.get(pk=1)
        OrderItem.objects.create(order=order, product=product, quantity=3)
        assert order.id == 3
        new_order_item_id = order.orderitem.all()[0].id
        assert new_order_item_id == 4

    def test_create_order_error(self):
        """Test creating an Order with invalid fields raises an error."""
        with pytest.raises(TypeError):
            Order.objects.create(total=1)

    def test_update_order_ok(self):
        """Test updating an existing Order with new OrderItems."""
        order: Order = Order.objects.get(pk=1)
        total_products = order.get_related_products().count()
        assert total_products == 2
        product: Product = Product.objects.get(pk=2)
        OrderItem.objects.create(order=order, product=product, quantity=6)
        total_products = order.get_related_products().count()
        assert total_products == 3

    def test_update_order_error(self):
        """Test updating Order with invalid datetime raises an error."""
        order: Order = Order.objects.get(pk=1)
        order.confirm_dt = "2024-16-11T13:30:46+00:00"
        with pytest.raises(ValidationError):
            order.save()

    def test_delete_order_ok(self):
        """Test deleting an existing Order instance successfully."""
        order: Order = Order.objects.get(pk=1).delete()
        assert order

    def test_delete_order_error(self):
        """Test deleting a non-existent Order raises an error."""
        with pytest.raises(ObjectDoesNotExist):
            Order.objects.get(pk=nex).delete()

    def test_update_payment_status(self):
        """Test updating "status" field of `Order` model after receiving payment."""
        order: Order = Order.objects.get(pk=1)
        assert order.status == order.STATUS_CHOICES["PENDING"]
        order.update_payment_status()
        order.save()
        assert order.status == order.STATUS_CHOICES["PAID"]

    def test_update_confirmation_status(self):
        """Test updating "status" field of `Order` model after receiving payment."""
        order: Order = Order.objects.get(pk=2)
        assert order.status == order.STATUS_CHOICES["PAID"]
        order.update_confirmation_status()
        order.save()
        assert order.status == order.STATUS_CHOICES["CONFIRMED"]

    @pytest.mark.usefixtures("create_mock_image")
    def test_orders_relationship(self, create_mock_image):
        """
        Test relationship between Order and OrderItem models by retrieving
        related products and creating new OrderItems.
        """
        order: Order = Order.objects.get(pk=1)
        order_products: Product = order.get_related_products()
        assert order_products[0].id == 1
        assert order_products[1].id == 2
        # Create new products, order items, and an order to test relationships
        new_order: Order = Order.objects.create()

        product_1: Product = Product.objects.create(
            name="new_test_product_1",
            picture=create_mock_image,
            content="test info 1",
            price=1000,
        )
        product_2: Product = Product.objects.create(
            name="new_test_product_2",
            picture=create_mock_image,
            content="test info 2",
            price=2500.50,
        )

        OrderItem.objects.create(order=new_order, product=product_1, quantity=5)
        OrderItem.objects.create(order=new_order, product=product_2, quantity=5)

        new_order_products: Product = new_order.get_related_products()
        assert new_order_products[0].id == 4
        assert new_order_products[1].id == 5
