from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny

from .serializers import UserSerializer, UserRegistrationSerializer

class UserRegistrationView(CreateAPIView):
    """view for user registration"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
