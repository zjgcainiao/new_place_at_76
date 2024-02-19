from django import forms
from talent_management.models import TalentsModel
from shift_management.models import Shift
from datetime import time
from django.forms.widgets import Select, DateInput, DateTimeInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, Hidden 

TIME_CHOICES = [(time(hour, minute), f"{hour:02d}:{minute:02d}")
                for hour in range(24) for minute in [0, 30]]
