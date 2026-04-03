from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from apps.products.models import Product

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity_kg', 1))

        product = Product.objects.get(id=product_id)

        cart, _ = Cart.objects.get_or_create(user=user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )

        if not created:
            item.quantity_kg += quantity
        else:
            item.quantity_kg = quantity

        item.save()

        return Response({"message": "Added to cart"})