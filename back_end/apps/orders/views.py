from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from back_end.apps.cart.models import Cart
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
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order
from .serializers import OrderSerializer


# ✅ Order History (User)
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# ✅ Order Detail
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ✅ Admin: Update Order Status
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        status_value = request.data.get('status')

        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        order.status = status_value
        order.save()

        return Response({"message": "Order status updated"})