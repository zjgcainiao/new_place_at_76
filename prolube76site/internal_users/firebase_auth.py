import os
import firebase_admin
from firebase_admin import credentials, auth
from rest_framework import authentication
from datetime import timezone
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError
from django.contrib.auth.models import User

prviate_key_json = "/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/2023-04-01-firebase-auth-private-key/fresh-start-9fdb6-firebase-adminsdk-yjbn6-92fef6fee6.json"

cred = credentials.Certificate(prviate_key_json)

default_firebase_app = firebase_admin.initialize_app(cred)

def firebase_new_user_by_email():
    if request.post=


# class FirebaseAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if not auth_header:
#             raise NoAuthToken("No auth token provided")

#         id_token = auth_header.split(" ").pop()
#         decoded_token = None
#         try:
#             decoded_token = auth.verify_id_token(id_token)
#         except Exception:
#             raise InvalidAuthToken("Invalid auth token")

#         if not id_token or not decoded_token:
#             return None

#         try:
#             uid = decoded_token.get("uid")
#         except Exception:
#             raise FirebaseError()

#         user, created = User.objects.get_or_create(username=uid)
#         user.profile.last_activity = timezone.localtime()

#         return (user, None)