from rest_framework import serializers

from orders.models import Order
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    cost = serializers.DecimalField(max_digits=25, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    payment_type = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["order", "cost", "status", "payment_type"]

    def create(self, validated_data):
        order = validated_data.get("order")
        payment = Payment.objects.create(
            order=order,
            cost=order.total_cost,
        )
        return payment
