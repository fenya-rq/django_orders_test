from rest_framework.viewsets import ModelViewSet

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
