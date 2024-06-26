from django import forms
import re
from appointments.models import AppointmentRequest, AppointmentImages
from datetime import date, datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from appointments.models import APPT_STATUS_PORGRESSING, APPT_STATUS_CONFIRMED, APPT_STATUS_SUBMITTED
from core_operations.utilities import deformat_phone_number
from core_operations.utilities import get_latest_vehicle_make_list, get_latest_vehicle_model_list
from homepageapp.models import MakesNewSQL02Model
from django.db.models import Q
from django.core.validators import FileExtensionValidator

from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from django.contrib.contenttypes.models import ContentType
from core_operations.constants import US_COUNTRY_CODE
from core_operations.utilities import format_phone_number_to_shop_standard
from appointments.custom_validators import validate_vehicle_year, validate_file_size, validate_phone_number
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox, ReCaptchaV3
