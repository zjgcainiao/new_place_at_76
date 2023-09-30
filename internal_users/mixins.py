from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden
from internal_users.models import InternalUser
from django.shortcuts import redirect
from django.contrib import messages


class InternalUserRequiredMixin(AccessMixin):
    """Mixin to ensure that the current user is authenticated and an instance of InternalUser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, "You need to be logged in to access this page.")
            return redirect('internal_users:internal_user_login')

        if not isinstance(request.user, InternalUser):
            messages.warning(
                request, "You do not have permission to view this page. Return to the homepage.")
            return redirect('homepageapp:homepage')

        return super().dispatch(request, *args, **kwargs)
