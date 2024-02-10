import os
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from internal_users.models import InternalUser
from firebase_auth_app.models import FirebaseUser
from customer_users.models import CustomerUser
from django.contrib import messages
import logging
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

logger = logging.getLogger('django')