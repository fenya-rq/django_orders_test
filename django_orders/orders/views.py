from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Order.objects.all().order_by("create_dt").select_related("orderitem")
    serializer_class = OrderSerializer
