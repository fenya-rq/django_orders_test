import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError

from conftest import _not_existing as nex
from orders.models import Order
from .models import Payment


@pytest.mark.django_db
class TestPayment:
    @pytest.fixture(autouse=True)
    def setup_method(self, load_fixture):
        load_fixture("products")
        load_fixture("orderstatuses")
        load_fixture("orders")
        load_fixture("orderitems")
        load_fixture("payments")

    def test_get_payment_ok(self):
        payment: Payment = Payment.objects.get(pk=1)
        assert isinstance(payment, Payment)

    def test_get_payment_error(self):
        with pytest.raises(ObjectDoesNotExist):
            Payment.objects.get(pk=nex)

    def test_create_payment_ok(self):
        order: Order = Order.objects.get(pk=1)
        payment: Payment = Payment.objects.create(order=order)
        assert isinstance(payment, Payment)

    def test_create_payment_error(self):
        with pytest.raises(ValueError):
            Payment.objects.create(order=1)

    def test_update_payment_ok(self):
        payment: Payment = Payment.objects.get(pk=1)
        assert payment.payment_type == "Bank Transfer"
        payment.payment_type = "PayPal"
        payment.save()
        assert payment.payment_type == "PayPal"

    def test_update_payment_error(self):
        payment: Payment = Payment.objects.get(pk=1)
        with pytest.raises(ValueError):
            payment.order = 3

    def test_delete_payment_ok(self):
        with pytest.raises(ProtectedError):
            payment: Payment = Payment.objects.get(pk=1).delete()
            assert payment.status == payment.VOIDED
