from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
