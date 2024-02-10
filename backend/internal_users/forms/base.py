# 2023-04-01 chatGPT generated form ---

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from internal_users.models import InternalUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from talent_management.models import TalentsModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox, ReCaptchaV3
from django.contrib.auth import authenticate
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, ButtonHolder, Submit, Row, Column, Button, Hidden
from crispy_forms.bootstrap import PrependedText, FormActions
import re