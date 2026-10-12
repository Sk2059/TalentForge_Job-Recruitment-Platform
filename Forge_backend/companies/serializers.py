from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(
        source = "owners.email",
        read_only = True,
    )
    class meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "website",
            "location",
            "industry",
            "company_size",
            "owner_email",
            "is_varified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "owner_email",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def create(self,validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)