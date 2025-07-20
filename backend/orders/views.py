from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions
from rest_framework.response import Response

from orders.models import Order, OrderItem
from users.models import CartItems
from store.models import Product

class PlaceOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # Get cart items for the current user with related product data

        # Reason for using select_related:
        # Optimize DB access: fetch related Product in same query to avoid N+1 problem
        # Without select_related, each item.product would trigger a separate DB query
        cart_items = CartItems.objects.select_related('product').filter(user=user)

        # Validate cart is not empty
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Pre-validate all cart items before creating order
        validation_errors = []
        total_amount = 0

        for item in cart_items:
            # Check if product still exists
            try:
                current_product = Product.objects.get(id=item.product.id)
            except Product.DoesNotExist:
                validation_errors.append(f"Product '{item.product.name}' no longer exists.")
                continue

            # Check inventory availability
            if item.quantity > current_product.inventory_count:
                validation_errors.append(
                    f"Insufficient inventory for '{current_product.name}'. "
                    f"Requested: {item.quantity}, Available: {current_product.inventory_count}."
                )
                continue

            # Calculate total with current prices
            total_amount += current_product.price * item.quantity

        # Return validation errors if any
        if validation_errors:
            return Response({"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST)

        # Validate total amount:
        if total_amount <= 0:
            return Response({"error": "Invalid order total amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Use database transaction to ensure atomicity
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=user, 
                    total_amount=total_amount, 
                    status=Order.Status.ORDERED
                )

                # Create order items and update inventory
                for item in cart_items:
                    # Get fresh product data to avoid race conditions:
                    # Example: If two users try to place an order for the same product at the same time, without this lock:
                    # Both may see that inventory is available, Both may proceed and inventory might become inconsistent
                    # .select_for_update(): locks the row(here, product row) for the duration of the transaction
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    
                    # Final inventory check within transaction
                    if item.quantity > product.inventory_count:
                        raise ValueError(f"Insufficient inventory for '{product.name}'.")
                    
                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        unit_price=product.price,
                    )
                    
                    # Update inventory
                    product.inventory_count -= item.quantity
                    product.save()

                # Clear cart only after successful order creation
                cart_items.delete()

            return Response({
                "message": "Order placed successfully.", 
                "order_id": order.id,
                "total_amount": str(total_amount)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Order processing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


