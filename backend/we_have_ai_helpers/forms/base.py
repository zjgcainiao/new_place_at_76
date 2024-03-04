from django import forms
import re
from appointments.models import AppointmentRequest, AppointmentImages
from datetime import date, datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button
from django.core.exceptions import ValidationError
