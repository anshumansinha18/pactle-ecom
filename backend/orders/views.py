from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions
from rest_framework.response import Response

from orders.models import Order, OrderItem
from users.models import CartItems

class PlaceOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        # 1. Get user from request
        user = request.user

        # 2. Get cart items for the current user:
        cart_items = CartItems.objects.filter(user=user)

        # 3. If cart is empty, return error:
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)


        # 4. Calculate total amount for cart items:
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # 5. Create a new order:
        order = Order.objects.create(user=user, total_amount=total_amount, status="ORDERED")

        # 6. Create OrderItems:
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
            )

        # Clear cart
        cart_items.delete()

        return Response({"message": "Order placed successfully."}, status=status.HTTP_201_CREATED)