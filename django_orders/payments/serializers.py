from rest_framework import serializers

from orders.models import Order
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=True
    )
    cost = serializers.DecimalField(max_digits=25, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)
    payment_type = serializers.CharField(max_length=25, default="Bank Transfer")

    class Meta:
        model = Payment
        fields = ["order", "cost", "status", "payment_type"]

    def create(self, validated_data) -> Payment:
        order = validated_data.pop("order")
        payment = Payment.objects.create(
            order=order,
            cost=order.total_cost, **validated_data
        )
        return payment

    def update(self, instance, validated_data) -> None:
        payment_type = validated_data.get("payment_type", instance.payment_type)
        instance.payment_type = payment_type
        instance.save(update_fields=["payment_type"])


