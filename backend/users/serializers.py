from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CartItems, CustomUser
import re

# ---------- LOGIN/SIGNUP ----------
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def validate_password(self, value):
        # Use Django's built-in password validators first
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        
        # Additional custom validation
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class AccessTokenOnlySerializer(TokenObtainPairSerializer):

    # runs when validating login credentials (username & password)
    def validate(self, attrs):

         # Calls the default logic: checks credentials and generates refresh and access token:
        data = super().validate(attrs)

        # Return only the access token (exclude refresh token)
        return {
            "access": data["access"]
        }



# ---------- CART ITEMS ----------
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ["id", "user", "product", "quantity"]
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def validate(self, data):
        # Check if product exists and validate against inventory
        product = data.get('product')
        quantity = data.get('quantity', 1)
        
        if product and quantity > product.inventory_count:
            raise serializers.ValidationError({
                'quantity': f'Cannot add {quantity} items. Only {product.inventory_count} available in inventory.'
            })
        
        return data