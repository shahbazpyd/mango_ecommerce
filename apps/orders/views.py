from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.cart.models import Cart
from .models import Order, OrderItem

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)

        items = cart.items.all()

        total_price = sum(
            item.product.price_per_kg * item.quantity_kg
            for item in items
        )

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            address=request.data.get('address'),
            city=request.data.get('city'),
            pincode=request.data.get('pincode'),
            phone=request.data.get('phone'),
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity_kg=item.quantity_kg,
                price_per_kg=item.product.price_per_kg
            )

        cart.items.all().delete()

        return Response({"message": "Order placed successfully"})