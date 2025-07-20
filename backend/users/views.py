from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from orders.serializers import OrderSerializer
from users.models import CartItems
from store.models import Product
from .serializers import AccessTokenOnlySerializer, CartItemSerializer, SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class SignupView(APIView):
    def post(self, request):

        # 1: Put request data into the serializer
        serializer = SignupSerializer(data=request.data)

        # 2. Check if data is valid
        if serializer.is_valid():
            # 3. Save user to database
            user = serializer.save()
            # 4. Return success response
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        # 5. Return error response if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):

    # This serializer handles username/password validation and generates JWT tokens
    # When user logs in successfully, it return access_token
    serializer_class = AccessTokenOnlySerializer



# ---------- CART ---------
class CartView(APIView):
    """
    This view handles whole collection of cart items
    It supports:
        - GET: retrieve all cart items for the current user
        - POST: create a new cart item for the current user
    """
    # Use JWT to authenticate the user from the request token:
    authentication_classes = [JWTAuthentication]

    # Allow access only to authenticated users:
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        cart_items = CartItems.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data.copy()
        user = request.user
        product_id = data.get("product")
        
        # Validate quantity input
        try:
            quantity = int(data.get("quantity", 1))
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid quantity value."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the same product is already in the user's cart
        existing_item = CartItems.objects.filter(user=user, product_id=product_id).first()

        if existing_item:
            # Check inventory for the new total quantity
            new_total_quantity = existing_item.quantity + quantity
            if new_total_quantity > product.inventory_count:
                return Response({
                    "error": f"Cannot add {quantity} more items. Only {product.inventory_count - existing_item.quantity} additional items available."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # If found, increment the quantity
            existing_item.quantity = new_total_quantity
            existing_item.save()
            serializer = CartItemSerializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # For new cart items, check inventory
        if quantity > product.inventory_count:
            return Response({
                "error": f"Cannot add {quantity} items. Only {product.inventory_count} available in inventory."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # If not found, create a new cart item
        data["user"] = user.id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetailView(RetrieveUpdateDestroyAPIView):
    """
    This view handles action on a specific cart item(just one at a time):
    IT supports:
        - GET: retrieve a single cart item
        - PUT: update a single cart item
        - DELETE: delete a single cart item
    """
    # Use JWT to authenticate the user from the request token:
    authentication_classes = [JWTAuthentication]

    # Allow access only to authenticated users:
    permission_classes = [permissions.IsAuthenticated]

    # Serializer used to update or return cart items
    serializer_class = CartItemSerializer

    # Filter cart items to only include items for the current user
    def get_queryset(self):
        return CartItems.objects.filter(user=self.request.user)



class UserOrderListView(APIView):
    """
    This view handles the list of orders for the current user:
    It supports:
        - GET: retrieve all orders for the current user
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all orders made by the logged-in user
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
