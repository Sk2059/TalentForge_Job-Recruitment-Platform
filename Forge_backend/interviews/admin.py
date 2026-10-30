

from django.contrib import admin
from .models import Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "application",
        "interview_type",
        "scheduled_at",
        "duration_minutes",
        "status",
        "created_at",
    )
    list_filter = (
        "interview_type",
        "status",
        "scheduled_at",
    )
    search_fields = (
        "application__candidate__email",
        "application__job__title",
        "application__job__company__name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "scheduled_at"