from django.shortcuts import render
from firebase_admin import credentials, auth
from firebase_auth_app.exceptions import NoAuthToken,InvalidAuthToken, FirebaseError
from firebase_auth_app.models import FirebaseUser
# Create your views here.
def firebase_authenticate(request):
        """Get the authorization Token, It raise exception when no authorization Token is given"""
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
                raise NoAuthToken("No auth token provided")
            """Decoding the Token It rasie exception when decode failed."""
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
                decoded_token = auth.verify_id_token(id_token)
        except Exception:
                raise InvalidAuthToken("Invalid auth token")
        """Return Nothing"""
        if not id_token or not decoded_token:
                return None
        """Get the uid of an user"""
        try:
                uid = decoded_token.get("uid")
        except Exception:
                raise FirebaseError()
        """Get or create the user"""

        user, created = FirebaseUser.objects.get_or_create(pk=uid)
        return (user, None)