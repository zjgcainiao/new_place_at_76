
from django.db.models import Q
import re
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.conf import settings
from internal_users.models import InternalUser
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from formtools.wizard.views import NamedUrlSessionWizardView
from formtools.preview import FormPreview
from django.http import HttpResponse
from talent_management.tasks import send_report_for_active_talents_with_pay_type_0
from core_operations.models import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, CURRENT_TIME_SHOW_PRECISE_TIME_WITH_TIMEZONE
from django.utils import timezone
from internal_users.mixins import InternalUserRequiredMixin
from talent_management.models import TalentsModel,TalentDocuments, TalentAudit
from talent_management.forms import TALENT_CREATE_FORMS, PersonalContactInfoForm, EmploymentInfoForm, RemarkAndCommentsForm, TalentUpdateForm
from talent_management.forms import TalentDocumentForm