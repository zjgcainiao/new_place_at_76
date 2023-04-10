from django import forms
from .models import AppointmentRequest


class AppointmentRequestForm(forms.ModelForm):
    appintment_vehicle_detail = forms.Textarea()
    class Meta:
        model = AppointmentRequest
        fields = ['appointment_date', 'appointment_reason_for_visit', 'appointment_first_name', 'appointment_last_name', 
                  'appointment_email', 'appointment_requested_datetime', 'appointment_vehicle_detail',
                  'appointment_concern_description']