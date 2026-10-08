from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserRegistrationSerializer,LogoutSerializer

class UserRegistrationView(CreateAPIView):
    """view for user registration"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class CurrentUserView(RetrieveUpdateDestroyAPIView):
    """view for current login user"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    """
    Blacklist the refresh token during logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT,)
