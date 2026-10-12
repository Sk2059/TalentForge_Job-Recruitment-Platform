from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "industry",
        "is_varified",
        "created_at"
    )
    list_filter =("is_varified","industry","company_size")
    search_fields = ("name","slug","owner__email")
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}