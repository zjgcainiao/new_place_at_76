
from django.http import HttpResponseForbidden
from internal_users.models import InternalUser
from django.shortcuts import redirect


class InternalUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Check if the URL resolves to a particular app, say url contain 'talents/'
        if 'talents/' in request.path:
            if not (request.user.is_authenticated and isinstance(request.user, InternalUser)):
                return redirect('internal_users:internal_user_login')

        return self.get_response(request)
