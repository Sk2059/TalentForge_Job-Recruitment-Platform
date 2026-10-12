from rest_framework.permissions import BasePermission

class IsCompanyOwner(BasePermission):
    """ Allow access only to recruiter who owns the company ."""
    message = "you do not have permissions to manage this company ."
    def has_object_permission(self,request,view,obj):
        return (
            request.user.is_authenticated
            and obj.owner_id == request.user.id
        )