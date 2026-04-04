from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.cart.models import Cart
from .models import Order, OrderItem

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        items = cart.items.all()

        if not items:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        required_fields = ['address', 'city', 'pincode', 'phone']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        total_price = sum(
            item.product.price_per_kg * item.quantity_kg
            for item in items
        )

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=request.data['address'],
            city=request.data['city'],
            pincode=request.data['pincode'],
            phone=request.data['phone'],
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity_kg=item.quantity_kg,
                price_per_kg=item.product.price_per_kg
            )

        items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id
        }, status=status.HTTP_201_CREATED)