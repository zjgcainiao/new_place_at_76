from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from appointments.models import AppointmentRequest
from django.template.loader import render_to_string
import logging
from django.core.mail import EmailMessage, get_connection, BadHeaderError
from urllib.parse import urljoin
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.db import models
from smtplib import SMTPException, SMTPAuthenticationError, SMTPServerDisconnected
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger('django')