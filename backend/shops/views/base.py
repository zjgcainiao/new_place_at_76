
import io
import requests
import stripe
import logging
import json
import uuid
import logging
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from shops.forms import LicensePlateSearchForm, VINSearchForm
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.views.decorators.csrf import csrf_exempt
from apis.utilities import database_sync_to_async
from apis.utilities import fetch_latest_vin_data_func
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.views.decorators.http import require_http_methods
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from urllib.parse import urljoin


# from shops.management.commands.load_stripe_products import Command
logger = logging.getLogger('django')

if (not settings.DEBUG) and settings.DJANGO_PROD_ENV == True:
    
    stripe.api_key = settings.STRIPE_SECRET_LIVE_KEY
else:
    # testing mode
    stripe.api_key = settings.STRIPE_SECRET_TEST_KEY

logger = logging.getLogger('external_api')