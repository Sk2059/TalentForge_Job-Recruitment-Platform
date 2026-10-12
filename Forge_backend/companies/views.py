from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser,JSONParser,MultiPartParser
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsRecruiter
from .models import Company
from .permissions import IsCompanyOwner
from .serializers import CompanySerializer

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.select_related("owner").all()
    serializer_class = CompanySerializer
    parser_classes = [JSONParser,FormParser,MultiPartParser]

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsRecruiter,IsAuthenticated]
        else:
              permission_classes = [
                IsAuthenticated,
                IsRecruiter,
                IsCompanyOwner,
            ]
        return [permission() for permission in permission_classes]