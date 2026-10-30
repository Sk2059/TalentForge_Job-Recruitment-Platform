from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Interview(models.Model):
    class InterviewType(models.TextChoices):
        PHONE = "phone" ,"Phone"
        VIDEO = "video", "Video"
        IN_PERSON = "in_person","In-Person"
        TECHNICAL = "technical","Technical"
        HR = "hr", "HR"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        RESCHEDULED = "rescheduled", "Rescheduled"

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.PROTECT,
        related_name="interviews",
    )

    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
        default=InterviewType.VIDEO,
    )

    scheduled_at = models.DateTimeField(
        db_index=True,
    )

    duration_minutes = models.PositiveSmallIntegerField(
        default=30,
    )

    meeting_link = models.URLField(
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    interviewer_notes = models.TextField(
        blank=True,
    )

    candidate_notes = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["scheduled_at"]
        indexes = [
            models.Index(
                fields=["application", "scheduled_at"],
                name="interview_app_date_idx",
            ),
            models.Index(
                fields=["status", "scheduled_at"],
                name="interview_status_date_idx",
            ),
        ]

    def clean(self):
        errors = {}

        if self.duration_minutes is not None and not (
            5 <= self.duration_minutes <= 480
        ):
            errors["duration_minutes"] = (
                "Interview duration must be between 5 and 480 minutes."
            )

        if (
            self.interview_type == self.InterviewType.VIDEO
            and not self.meeting_link
        ):
            errors["meeting_link"] = (
                "A meeting link is required for video interviews."
            )

        if (
            self.interview_type == self.InterviewType.IN_PERSON
            and not self.location
        ):
            errors["location"] = (
                "A location is required for in-person interviews."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return (
            f"{self.application.candidate.email} — "
            f"{self.application.job.title} — "
            f"{self.scheduled_at:%Y-%m-%d %H:%M}"
        )


