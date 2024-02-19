from django import forms
from talent_management.models import TalentsModel, TalentDocuments
from datetime import date
from django.db.models import Q
# version 1 - talent creation form
from core_operations.common_functions import generate_today_date_format
from core_operations.constants import LIST_OF_STATES_IN_US
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button
from django.utils.translation import gettext_lazy 