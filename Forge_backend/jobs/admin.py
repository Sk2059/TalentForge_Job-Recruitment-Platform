from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "employment_type",
        "workplace_type",
        "is_published",
        "created_at",
    )
    list_filter = (
        "employment_type",
        "workplace_type",
        "experience_level",
        "is_published",
    )
    search_fields = ("title", "company__name", "location")
    readonly_fields = ("created_at", "updated_at", "published_at")
