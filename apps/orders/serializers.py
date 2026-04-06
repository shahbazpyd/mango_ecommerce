from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity_kg', 'price_per_kg']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'status',
            'address',
            'city',
            'pincode',
            'phone',
            'created_at',
            'items'
        ]