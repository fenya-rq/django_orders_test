import pytest

from orders.models import Order
from . import OrderAdminRequest


@pytest.mark.django_db
class TestOrderAdminRequest:
    """
    Test suite for the OrderAdminRequest class.

    Uses pytest-django's database support to test the interaction
    with Django's database models and to simulate real request
    scenarios for the OrderAdminRequest class.
    """

    url = "https://httpbin.org/post"
    order_obj: Order
    request_handler: OrderAdminRequest

    @pytest.fixture(autouse=True)
    def setup_method(self, load_fixture):
        """
        Fixture to automatically set up test data before each test.

        It loads the 'orders' fixture, retrieves an order object by
        its primary key, and initializes the request handler instance
        with the test order and URL.
        """
        load_fixture("orders")
        self.order_obj = Order.objects.get(pk=2)
        self.request_handler = OrderAdminRequest(self.order_obj, self.url)

    def test_build_json_object(self):
        """
        Tests if build_json_object method correctly returns a dictionary.

        Ensures that the order data is serialized into a valid dictionary
        which is necessary for sending the correct payload in the request.
        """
        result = self.request_handler.build_json_object()
        assert isinstance(result, dict)

    def test_send_post_request_ok(self):
        """
        Tests if send_request method successfully handles a POST request.

        Simulates sending order data to a valid external URL and checks if
        the request is processed with a 2xx status code.
        """
        result = self.request_handler.send_request()
        assert result is True

    def test_send_post_request_error(self):
        """
        Tests how send_request handles errors with invalid URLs.

        Simulates sending order data to an invalid URL and expects the
        request to fail, returning False.
        """
        url = "https:google.com"
        request_handler = OrderAdminRequest(self.order_obj, url)
        result = request_handler.send_request()
        assert result is False
