from rest_framework.permissions import BasePermission

class IsJobCompanyOwner(BasePermission):
    message = "you do have permission to manage this job "

    def has_object_permission(self,request,view,obj):
        return (
            request.user.is_authenticated
            and obj.company.owner_id == request.user.id
        )