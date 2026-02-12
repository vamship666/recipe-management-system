from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(APIView):
    # Public endpoint to register new users (creator/viewer)
    permission_classes = []

    def post(self, request):
        # Validate incoming registration data
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Save user if validation passes
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # Public endpoint to authenticate users and return token
    permission_classes = []

    def post(self, request):
        # Validate login credentials
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            # Return authentication token on successful login
            return Response({
                "token": serializer.validated_data["token"]
            })

        # Return error if credentials are invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
