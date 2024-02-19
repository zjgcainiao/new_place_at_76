import os
import calendar
import json
from homepageapp.models import ModelsNewSQL02Model
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
# repairOrder model was added on 11/5/2022. Deleted on 11/18/2022
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin

from appointments.models import AppointmentRequest, AppointmentImages
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from formtools.wizard.views import WizardView
from django.urls import reverse_lazy


from appointments.models import APPT_STATUS_CANCELLED, APPT_STATUS_NOT_SUBMITTED
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from appointments.models import APPT_STATUS_SUBMITTED

from appointments.forms import AppointmentCreationForm, AppointmentImagesForm
from appointments.forms import AppointmentImageFormset

from formtools.wizard.views import SessionWizardView