
from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):
    message = "Only candidates can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="Candidate").exists()
        )


class IsRecruiter(BasePermission):
    message = "Only recruiters can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="Recruiter").exists()
        )


class IsCandidateOrRecruiter(BasePermission):
    message = "Only candidates and recruiters can access applications."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.groups.filter(
            name__in=["Candidate", "Recruiter"]
        ).exists()


class IsApplicationCandidate(BasePermission):
    message = "You can access only your own applications."

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.candidate_id == request.user.id
        )


class IsJobCompanyRecruiter(BasePermission):
    message = "You can manage applications only for jobs belonging to your companies."

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.job.company.owner_id == request.user.id
        )