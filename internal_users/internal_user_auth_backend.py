
from django.contrib.auth.backends import BaseBackend
from internal_users.models import InternalUser


class InternalUserBackend(BaseBackend):

    def authenticate(self, request, email, password=None, **kwargs):
        try:
            internal_user = InternalUser.objects.get(email=email)
        except InternalUser.DoesNotExist:
            return None

        if internal_user.check_password(password):
            # check if it's the superuser
            if internal_user.is_active and internal_user.is_staff:
                return internal_user
            elif internal_user.is_active:
                return internal_user
        return None

    def get_user(self, user_id):
        try:
            return InternalUser.objects.get(pk=user_id)
        except InternalUser.DoesNotExist:
            return None
