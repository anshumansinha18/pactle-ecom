from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

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
