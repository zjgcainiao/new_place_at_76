
from .base import ListView
from appointments.models import AppointmentRequest

class AppointmentOfNext7DaysListView(ListView):
    template_name = 'dashboard/13_appointment_last_7_day_display.html'
    model = AppointmentRequest
    context_object_name = 'appointments'
