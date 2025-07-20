from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "inventory_count", "image_url"]
    
    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Product name cannot be empty.")
        return value.strip()
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    
    def validate_inventory_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory count cannot be negative.")
        return value
