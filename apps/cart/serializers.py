from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)
    price_per_kg = serializers.DecimalField(
        source='product.price_per_kg',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'quantity_kg',
            'price_per_kg',
            'total_price'
        ]

    def get_total_price(self, obj):
        return obj.product.price_per_kg * obj.quantity_kg


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cart_price']

    def get_total_cart_price(self, obj):
        return sum(
            item.product.price_per_kg * item.quantity_kg
            for item in obj.items.all()
        )