import re
import random
import time
from abc import ABC, abstractmethod

import requests

from django_orders import settings
from orders.serializers import OrderSerializer


class BaseExternalRequestManager(ABC):
    """
    Abstract base class for handling external requests. Subclasses must
    implement the send_request method.
    """

    @abstractmethod
    def send_request(self):
        pass


class OrderAdminRequest(BaseExternalRequestManager):
    """
    Handles the request logic for sending order data to an external
    service.
    """

    def __init__(self, order_obj, url: str = settings.SEND_ORDER_DATA_URL) -> None:
        """
        Initializes the request handler with an order object
        and optional URL.

        :param order_obj: The order object containing data to be sent.
        :param url: The external service URL where the order data will
         be sent. Defaults to the value from
         settings.SEND_ORDER_DATA_URL.
        """
        self.order_obj = order_obj
        self.url = url

    def build_json_object(self) -> dict:
        """
        Builds the JSON object from the order serializer data to be sent
        in the request.
        """
        sr_data = OrderSerializer(self.order_obj).data
        result = {
            "id": sr_data["id"],
            "cost": sr_data["total_cost"],
            "confirm_dt": sr_data["confirm_dt"],
        }
        return result

    def send_request(self) -> bool:
        """
        Sends a POST request with order data to the external service.
        Attempts the request up to 3 times if it fails. Returns True
        if the request succeeds (i.e., status code starts with '20'),
        otherwise returns False.
        """
        order_data = self.build_json_object()
        # Imitation request processing
        random_request_time = round(random.random(), 2)
        time.sleep(random_request_time)

        attempts = 3
        while attempts:
            try:
                r = requests.post(self.url, order_data)
                print(r.status_code)
                if re.match(r"^20\d$", str(r.status_code)):
                    return True
                return False
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                attempts -= 1
        return False
