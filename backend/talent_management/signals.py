# this file incldues the signals related to creating, updating and deleting an employee record
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from talent_management.models import TalentsModel, TalentAudit
from internal_users.models import InternalUser
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from internal_users.token_generators import AccountActivationTokenGenerator, account_activation_token
from internal_users.token_generators import create_activation_token
import logging
from urllib.parse import urljoin
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


logger = logging.getLogger('django')


