import jwt
from datetime import datetime, timedelta
from django.conf import settings

# creation a JWT enabled token. Token expires in 14 days
def create_activation_token_for_customer_user(user):
    
    # Token expires in 14 day (you can adjust this)
    expiration = datetime.utcnow() + timedelta(days=14)

    payload = {
        'user_id': user.pk,
        'email_verified': user.cust_user_email_verified,
        'exp': expiration,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token

# the decoding method to decode the JWT token used for user activation
def decode_activation_token_for_customer_user(token):
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
