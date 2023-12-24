from rest_framework.permissions import IsAuthenticated
from internal_users.models import InternalUser
from rest_framework import permissions
from customer_users.models import CustomerUser

class IsInternalUser(permissions.BasePermission):
    """
    Custom permission to only allow internal users to view the dashboard.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, InternalUser)

class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow customer users to view customer user dashboard.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, CustomerUser)
