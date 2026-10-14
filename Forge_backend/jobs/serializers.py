from django.utils import timezone
from rest_framework import serializers

from companies.models import Company
from .models import Job

class JobSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source = "company.name",
        read_only = True
    )
    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_name",
            "title",
            "slug",
            "description",
            "responsibilities",
            "requirements",
            "employment_type",
            "workplace_type",
            "experience_level",
            "location",
            "salary_min",
            "salary_max",
            "salary_currency",
            "application_deadline",
            "is_published",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "company_name",
            "published_at",
            "created_at",
            "updated_at",
        ]
    def validate_company(self,company):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication is required"
            )

        if company.user_id != request.user_id :
            raise serializers.ValidationError(
                "You can only create jobs for companies you own."
            )
        return company
    
    def validate(self, attrs):
        salary_min = attrs.get(
            "salary_min",
            getattr(self.instance, "salary_min", None),
        )
        salary_max = attrs.get(
            "salary_max",
            getattr(self.instance, "salary_max", None),
        )

        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise serializers.ValidationError({
                "salary_max": (
                    "Maximum salary must be greater than "
                    "or equal to minimum salary."
                )
            })
        return attrs

    def create(self,validated_data):
        if validated_data.get("is_published",False):
            validated_data["published_at"]= timezone.now()

        return super().create(validated_data)

    def update(self,instance,validated_data):
        was_published = instance.is_published

        will_be_published = validated_data.get(
            "is_published",
            was_published,
        )
        if will_be_published and not was_published:
            validated_data["published_at"] = timezone.now()
        elif not will_be_published and was_published:
            validated_data["published_at"] = None

        return super().update(instance,validated_data)
