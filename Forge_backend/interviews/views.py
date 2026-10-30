from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.models import Application
from .models import Interview
from .permissions import (
    IsCandidateOrRecruiter,
    IsRecruiter
)
from .serializers import InterviewSerializer

class InterviewViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class= InterviewSerializer

    def get_permissions(self):
        if self.action in ["create","update","partial_update","cancel"]:
            permission_classes = [
                IsAuthenticated,
                IsRecruiter,
            ]
        else:
            permission_classes=[
                IsAuthenticated,
                IsCandidateOrRecruiter,
            ]
        return [
            permission()
            for permission in permission_classes
        ]
    def get_queryset(self):
        user = self.request.user

        queryset = Interview.objects.select_related(
            "application",
            "application__candidate",
            "application__job",
            "application__job__company",
        )

        if not user.is_authenticated:
            return queryset.none()

        is_candidate = user.groups.filter(
            name ="Candidate"
        ).exists()

        is_recruiter = user.groups.filter(
            name = "Recruiter"
        ).exists()

        if is_candidate and is_recruiter:
            return queryset.filter(
                Q(application__candidate=user)
                | Q(application__job__company__owner=user)
            ).distinct()

        if is_candidate:
            return queryset.filter(
                application__candidate=user
            )

        if is_recruiter:
            return queryset.filter(
                application__job__company__owner=user
            )

        return queryset.none()

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Application = serializer.validated_data["application"]

        if application.job.company.owner_id != request.user.id:
            raise ValidationError({
                "application": (
                    "You can only schedule interviews for applications "
                    "belonging to your own company's jobs."
                )
            })

        with transaction.atomic():
            authorized_application = (
                Application.object.select_for_update()
                .filter(
                    pk = application.pk,
                    job__company__owner = request.user,
                )
                .first()
            )

            if authorized_application is None:
                raise ValidationError({
                    "application":"the application is unavailable"
                })

            interview = serializer.save(
                application = authorized_application
            )
        output_serializer = self.get_serializer(interview)

        return Response(
            output_serializer.data,
            status = status.HTTP_201_CREATED,
        )

    def partial_update(self, request, *args, **kwargs):
        return self._update_interview(
            request,
            partial=True,
            **kwargs,
        )

    def partial_update(self, request, *args, **kwargs):
        return self._update_interview(
            request,
            partial=True,
            **kwargs,
        )

    def _update_interview(self, request, partial, **kwargs):
        interview = self.get_object()

        if interview.status in [
            Interview.Status.COMPLETED,
            Interview.Status.CANCELLED,
        ]:
            raise ValidationError({
                "status": (
                    "Completed or cancelled interviews cannot be modified."
                )
            })

        serializer = self.get_serializer(
            interview,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
    )
    def cancel(self, request, pk=None):
        interview = self.get_object()

        if interview.status == Interview.Status.CANCELLED:
            raise ValidationError({
                "status": "This interview has already been cancelled."
            })

        if interview.status == Interview.Status.COMPLETED:
            raise ValidationError({
                "status": "A completed interview cannot be cancelled."
            })

        interview.status = Interview.Status.CANCELLED
        interview.save(update_fields=["status", "updated_at"])

        return Response(
            self.get_serializer(interview).data,
            status=status.HTTP_200_OK,
        )