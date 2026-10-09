from rest_framework.permissions import BasePermission

class HasTalentForgeGroup(BasePermission):
    required_group = None

    def has_permission(self,request,view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.required_group
            and user.groups.filter(
                name = self.required_group
            ).exists()
        )

class IsCandidate(HasTalentForgeGroup):
    required_group = "Candidate"

class IsRecruiter(HasTalentForgeGroup):
    required_group = "Recruiter"