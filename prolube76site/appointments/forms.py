from django import forms
from .models import AppointmentRequest
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

class AppointmentRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'appointment_requested_datetime',
                'appointment_reason_for_visit',
                'appointment_first_name',
                'appointment_last_name',
                'appointment_email',
                'appointment_concern_description',
                ),
            Field('appointment_email', id="appointment_email_field", css_class= "form-control" ),
            Submit('submit', 'Submit', css_class='btn btn-outline-danger'),
        )
    
    class Meta:
        model = AppointmentRequest
        fields = [
            'appointment_requested_datetime',
            'appointment_reason_for_visit',
            'appointment_first_name',
            'appointment_last_name',
            'appointment_email',
            'appointment_vehicle_detail',
            'appointment_concern_description',
        ]
        widgets = {
            'appointment_requested_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'}),
            'appointment_first_name': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'appointment_last_name': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'appointment_reason_for_visit': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'appointment_vehicle_detail': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'appointment_email': forms.EmailInput(attrs={'type': 'text','class': 'form-control'}),
            'appointment_concern_description': forms.Textarea(attrs={'type': 'text','class': 'form-control'}),
        }

        labels = {
            'appointment_requested_datetime': _('Requested Date and Time'),
            'appointment_reason_for_visit': _('Reason for Visit'),
            'appointment_first_name': _('First Name'),
            'appointment_last_name': _('Last Name'),
            'appointment_email': _('Email'),
            'appointment_vehicle_detail': _('Vehicle Detail'),
            'appointment_concern_description': _('Description of Concern'),
        }