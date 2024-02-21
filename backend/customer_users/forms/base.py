from django import forms
from customer_users.models import CustomerUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re
from django.core.validators import RegexValidator
# import common functions from common_functions.py
# testing to combine common functions into one centralized location.
from core_operations.utilities import is_valid_us_phone_number
from core_operations.constants import LIST_OF_STATES_IN_US
from core_operations.validators import validate_us_state, validate_zip_code
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox, ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Button, ButtonHolder, Submit,HTML
