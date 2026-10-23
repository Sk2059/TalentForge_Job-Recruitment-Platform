from django.utils import timezone
from rest_framework import serializers

from jobs.models import Job
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(
        source = "candidate.email",
        read_only = True,
    )
    job_title = serializers.CharField(
        source="job.title",
        read_only = True,
    )
    company_name = serializers.CharField(
        source = "job.company.name",
        read_only = True,
    )

    class Meta:
        model = Application
        fields = [
             "id",
            "candidate",
            "candidate_email",
            "job",
            "job_title",
            "company_name",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]
        read_only_fields =[
            "id",
            "candidate",
            "candidate_email",
            "job_title",
            "company_name",
            "status",
            "applied_at",
            "updated_at",
        ]

    def validate_job(self,Job):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication is required for the job"
                )

        if not Job.is_published:
            raise serializers.ValidationError(
                "you can only apply for published jobs"
            )

        if (
            Job.application_deadline is not None
            and Job.application_deadline < timezone.localdate()
        ):
            raise serializers.ValidationError(
                "The application deadline for this job has passed."
            )
        return Job

    def validate(self, attrs):
        if self.instance is None:
            request = self.context.get("request")
            job = attrs.get("job")

            if request and job and Application.objects.filter(
                candidate=request.user,
                job=job,
            ).exists():
                raise serializers.ValidationError({
                    "job": "You have already applied for this job."
                })
        return attrs
    
    def create(self, validated_data):
        request = self.context["request"]

        return Application.objects.create(
            candidate=request.user,
            **validated_data,
        )

class ApplicationStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[
            (status.value, status.label)
            for status in Application.Status
            if status != Application.Status.WITHDRAWN
        ]
    )
    class Meta:
        model = Application
        fields = ["status"]

    def validate_status(self, value):
        if self.instance.status == Application.Status.WITHDRAWN:
            raise serializers.ValidationError(
                "A withdrawn application cannot be reopened."
            )

        return value