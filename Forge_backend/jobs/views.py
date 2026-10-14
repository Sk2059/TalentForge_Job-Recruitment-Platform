from django.db.models import Q
from rest_framework.parsers import FormParser,JSONParser,MultiPartParser
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsRecruiter
from .models import Job
from .serializers import JobSerializers
from .permissions import IsJobCompanyOwner

class JobViewSet(ModelViewSet):
    serializer_class = JobSerializers
    parser_classes = [FormParser,JSONParser,MultiPartParser]

    def get_queryset(self):
        queryset= Job.objects.select_related(
            "company",
            "company__owner"
        )

        user = self.request.user

# Public users see published jobs only.
        if not user.is_authenticated:
            return queryset.filter(is_published=True)

# Recruiters can also see their own unpublished drafts.
        is_recruiter = user.groups.filter(name="Recruiter").exists()

        if is_recruiter:
            return queryset.filter(
                Q(is_published=True) | Q(company__owner=user)
            ).distinct()

        return queryset.filter(is_published=True)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsRecruiter]
        else:
            permission_classes = [
                IsAuthenticated,
                IsRecruiter,
                IsJobCompanyOwner,
            ]

        return [permission() for permission in permission_classes]



        