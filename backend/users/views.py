from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccessTokenOnlySerializer, SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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