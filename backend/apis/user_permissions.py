from rest_framework.permissions import IsAuthenticated, BasePermission
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
import datetime
from django.utils import timezone


class IsInternalUser(BasePermission):
    """
    Custom permission to only allow internal users to view the dashboard.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, InternalUser)


class IsCustomerUser(BasePermission):
    """
    Custom permission to only allow customer users to view customer user dashboard.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, CustomerUser)


class LicenseVinSearchPermission(BasePermission):
    message = 'Search limit reached.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Logic to check and update the count for authenticated user
            # Allow double the number of searches
            return False
        else:
            # Logic for unauthenticated users
            return handle_anonymous_user_license_vin_search(request)


def handle_anonymous_user_license_vin_search(request):
    reset_interval = datetime.timedelta(days=182)  # Reset
    limit = 3

    search_count = request.session.get('plate_vin_search_count', 0)
    last_reset_str = request.session.get('plate_vin_search_last_reset', None)

    # Convert last_reset from string to datetime
    if last_reset_str:
        last_reset = datetime.datetime.fromisoformat(last_reset_str)
    else:
        # If last_reset isn't in the session, initialize it to now
        last_reset = timezone.now()

    # Check if the interval has passed and reset if necessary
    if timezone.now() - last_reset > reset_interval:
        search_count = 0
        last_reset = timezone.now()
        request.session['plate_vin_search_last_reset'] = last_reset.isoformat()

    # Check if the user is within their search limit
    if search_count < limit:
        request.session['plate_vin_search_count'] = search_count + 1
        return True
    else:
        return False


class IsPaidUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.auth.get('is_paid_user', False)
