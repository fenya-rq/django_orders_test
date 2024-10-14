from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from .models import Order, OrderStatus


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ["products", "total_cost", "status", "create_dt", "confirm_dt"]

    def create(self, validated_data):
        products_list = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        products = [Product.objects.get(id=product["id"]) for product in products_list]
        order.products.set(products)  # Associate products with the order
        return order
