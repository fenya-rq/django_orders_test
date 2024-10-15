from rest_framework import serializers

from products.models import Product
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(
        max_digits=25, decimal_places=2, read_only=True
    )
    create_dt = serializers.DateTimeField(read_only=True)
    confirm_dt = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    orderitem = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["total_cost", "status", "create_dt", "confirm_dt", "orderitem"]

    def create(self, validated_data):
        products_list = validated_data.pop("orderitem")
        order = Order.objects.create(**validated_data)
        for product in products_list:
            OrderItem.objects.create(
                order=order, product=product["product"], quantity=product["quantity"]
            )
        return order
