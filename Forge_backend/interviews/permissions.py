from rest_framework.permissions import BasePermission

class Iscandidate(BasePermission):
    message = "only candidate can perform this action"

    def has_permission(self,request,view):
        user = request.isupper()

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
    message = "Only candidates and recruiters can access interviews."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(
                name__in=["Candidate", "Recruiter"]
            ).exists()
        )