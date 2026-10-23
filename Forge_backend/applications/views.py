from django.db import IntegrityError,transaction
from django.db.models import Q
from rest_framework import status 
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser,JSONParser,MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin
)
from .models import Application
from .permissions import (
    IsCandidate,
    IsRecruiter,
    IsCandidateOrRecruiter,
    IsApplicationCandidate,
    IsJobCompanyRecruiter
)
from .serializers import (
    ApplicationSerializer,
    ApplicationStatusSerializer,
)

class ApplicationViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = ApplicationSerializer
    parser_classes = [FormParser,JSONParser,MultiPartParser]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsCandidate]
        elif self.action == "list":
            permission_classes = [IsAuthenticated,IsCandidateOrRecruiter]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsCandidateOrRecruiter]
        elif self.action == "update_status":
            permission_classes =[
                 IsAuthenticated,
                IsRecruiter,
                IsJobCompanyRecruiter,
            ]
        elif self.action == "withdraw":
            permission_classes =[
                IsAuthenticated,
                IsCandidate,
                IsApplicationCandidate,
            ]
        else :
            permission_classes = [IsAuthenticated]

        return  [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.select_related(
            "candidate",
            "job",
            "job__company",
        )

        if not user.is_authenticated:
            return queryset.none()

        is_candidate = user.groups.filter(name="Candidate").exists()
        is_recruiter = user.groups.filter(name="Recruiter").exists()

        if is_candidate and is_recruiter:
            return queryset.filter(
                Q(candidate=user) | Q(job__company__owner=user)
            ).distinct()

        if is_candidate:
            return queryset.filter(candidate=user)

        if is_recruiter:
            return queryset.filter(job__company__owner=user)

        return queryset.none()

    def get_serializer_class(self):
        if self.action == "update_status":
            return ApplicationStatusSerializer

        return ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)

        except IntegrityError:
            job = serializer.validated_data.get("job")

            if job and Application.objects.filter(
                candidate=request.user,
                job=job,
            ).exists():
                raise ValidationError({
                    "job": "You have already applied for this job."
                })

            raise

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="status",
    )
    def update_status(self, request, pk=None):
        application = self.get_object()

        serializer = self.get_serializer(
            application,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            ApplicationSerializer(
                application,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="withdraw",
    )
    def withdraw(self, request, pk=None):
        application = self.get_object()

        if application.status == Application.Status.WITHDRAWN:
            raise ValidationError({
                "status": "This application has already been withdrawn."
            })

        if application.status in [
            Application.Status.ACCEPTED,
            Application.Status.REJECTED,
        ]:
            raise ValidationError({
                "status": (
                    "You cannot withdraw an application that has already "
                    "been accepted or rejected."
                )
            })

        application.status = Application.Status.WITHDRAWN
        application.save(update_fields=["status", "updated_at"])

        return Response(
            ApplicationSerializer(
                application,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
