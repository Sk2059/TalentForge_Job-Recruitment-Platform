from django.utils import timezone
from rest_framework import serializers
from applications.models import Application
from .models import Interview

class InterviewSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(
        source="application.candidate.email",
        read_only = True,
    )
    job_title = serializers.CharField(
        source = "application.job.title",
        read_only = True,
    )
    company_name = serializers.CharField(
        source ="application.job.company.name",
        read_only = True,
    )
    class Meta:
        model = Interview

        fields = [
            "id",
            "application",
            "candidate_email",
            "job_title",
            "company_name",
            "interview_type",
            "scheduled_at",
            "duration_minutes",
            "meeting_link",
            "location",
            "interviewer_notes",
            "candidate_notes",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate_email",
            "job_title",
            "company_name",
            "interviewer_notes",
            "candidate_notes",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_fields(self):
        fields = super().get_fields()

        # An existing interview cannot be reassigned to another application.
        if self.instance is not None:
            fields["application"].read_only = True

        return fields
    

    def validate_duration_minutes(self, value):
        if not 5 <= value <= 480:
            raise serializers.ValidationError(
                "Interview duration must be between 5 and 480 minutes."
            )

        return value

    def validate_scheduled_at(self, value):
        if self.instance is None and value <= timezone.now():
            raise serializers.ValidationError(
                "An interview must be scheduled for a future date and time."
            )

        return value

    def validate(self, attrs):
        interview_type = attrs.get(
            "interview_type",
            getattr(
                self.instance,
                "interview_type",
                Interview.InterviewType.VIDEO,
            ),
        )

        meeting_link = attrs.get(
            "meeting_link",
            getattr(self.instance, "meeting_link", ""),
        )

        location = attrs.get(
            "location",
            getattr(self.instance, "location", ""),
        )

        errors = {}

        if (
            interview_type == Interview.InterviewType.VIDEO
            and not meeting_link
        ):
            errors["meeting_link"] = (
                "A meeting link is required for video interviews."
            )

        if (
            interview_type == Interview.InterviewType.IN_PERSON
            and not location
        ):
            errors["location"] = (
                "A location is required for in-person interviews."
            )
        if errors:
            raise serializers.ValidationError(errors)

        return attrs
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            is_recruiter = request.user.groups.filter(
                name="Recruiter"
            ).exists()

            if not is_recruiter:
                data.pop("interviewer_notes", None)

        return data