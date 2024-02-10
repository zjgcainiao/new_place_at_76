from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from customer_users.models import CustomerUser
from internal_users.models import InternalUser
from django.shortcuts import redirect
from django.contrib import messages

# this middleware is not completed. 2023-10-13
class CustomerUserRequiredMixin(AccessMixin):
    """Mixin to ensure that the current user is authenticated and an instance of CustomerUser"""

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(
                request, "You need to be logged in to access this page.")
            return redirect('customer_users:customer_user_login')

        if isinstance(user, InternalUser) and user.is_authenticated:
            messages.warning(
                request, "Employee(s) cannot view this page. Please log out first and try again.")
            return redirect('internal_users:internal_user_logout')
        if not isinstance(user, CustomerUser) and not isinstance(user, InternalUser) and user.is_authenticated:
            messages.warning(
                request, "Unknown user type. No Permission to this page.")
            return redirect('homepageapp:homepage')

        return super().dispatch(request, *args, **kwargs)
