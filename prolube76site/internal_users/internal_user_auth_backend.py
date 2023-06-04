
from django.contrib.auth.backends import BaseBackend
from internal_users.models import InternalUser

class InternalUserBackend(BaseBackend):

    def authenticate(self, request, email, password=None, **kwargs):
        try:
            internal_user = InternalUser.objects.get(email=email)
            if internal_user.check_password(password):
                return internal_user
        except InternalUser.DoesNotExist:
            return None
        

    def get_user(self, user_id):
        try:
            return InternalUser.objects.get(pk=user_id)
        except InternalUser.DoesNotExist:
            return None