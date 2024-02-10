from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.user_is_active))


account_activation_token = AccountActivationTokenGenerator()

# creation a JWT enabled token. Token expires in 14 days
def create_activation_token(user):
    # Token expires in 14 day (you can adjust this)
    expiration = datetime.utcnow() + timedelta(days=14)

    payload = {
        'user_id': user.pk,
        'is_active': user.user_is_active,
        'exp': expiration
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token

# the decoding method to decode the JWT token used for user activation


def decode_activation_token(token):
    try:
        decoded_payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.DecodeError:
        # Token is invalid
        return None
