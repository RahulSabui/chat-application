from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer
)
from accounts.services.auth_service import AuthService

from core.utils import api_response


class RegisterAPIView(APIView):

    permission_classes = []

    authentication_classes = []

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            tokens = AuthService.generate_tokens(user)

            return api_response(
                success=True,
                message="Registration successful.",
                data={
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "tokens": tokens,
                },
                status_code=status.HTTP_201_CREATED,
            )

        return api_response(
            success=False,
            message="Validation failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
class LoginAPIView(APIView):

    permission_classes = []

    authentication_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            tokens = AuthService.generate_tokens(user)

            return api_response(
                success=True,
                message="Login successful.",
                data={
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "tokens": tokens,
                },
            )

        return api_response(
            success=False,
            message="Login failed.",
            errors=serializer.errors,
            status_code=400,
        )

class LogoutAPIView(APIView):

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:

            AuthService.blacklist_token(
                serializer.validated_data["refresh"]
            )

            return api_response(
                message="Logout successful."
            )

        except Exception:

            return api_response(
                success=False,
                message="Invalid refresh token.",
                status_code=400,
            )