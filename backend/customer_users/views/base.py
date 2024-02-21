import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from customer_users.forms import CustomerUserRegistrationForm, CustomerUserLoginForm
from customer_users.customer_auth_backend import CustomerUserBackend
from customer_users.models import CustomerUser
from formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from firebase_admin import auth
from customer_users.tasks import create_customer_user_from_firebase_auth, create_firebase_auth_user
from firebase_auth_app.models import FirebaseUser
from asgiref.sync import sync_to_async
from apis.utilities import database_sync_to_async

from customer_users.token_generators import decode_activation_token_for_customer_user, create_activation_token_for_customer_user

logger = logging.getLogger('django')
