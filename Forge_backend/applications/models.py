from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWING = "reviewing", "Under Review"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        ACCEPTED = "accepted", "Accepted"
        WITHDRAWN = "withdrawn", "Withdrawn"

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="job_applications"
    )

    job = models.ForeignKey(
        "jobs.job",
        on_delete=models.PROTECT,
        related_name="applications"
    )

    resume = models.FileField(
        upload_to="application_resume/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf","doc","docx"]
            )
        ],
        blank=True,
        null=True
    )

    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=55,
        choices=Status.choices,
        default = Status.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job"],
                 name="unique_candidate_job_application",
            )
        ]
        indexes = [
             models.Index(
                fields=["job", "status"],
                name="app_job_status_idx",
            ),
            models.Index(
                fields=["candidate", "-applied_at"],
                name="app_candidate_date_idx",
            ),
        ]

    def __str__(self):
        return f"{self.candidate.email} — {self.job.title}"
