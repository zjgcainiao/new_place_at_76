from .base import render, get_object_or_404, TemplateView
from appointments.models import AppointmentRequest, AppointmentImages


class AppointmentSuccessView(TemplateView):
    template_name = 'appointments/22_appointment_creation_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment_data = self.request.session.get('appointment_data', {})
        if appointment_data:
            appointment = AppointmentRequest(**appointment_data)
            appointment.save()
            self.request.session['appointment_data'] = None
            context['appointment'] = appointment
            # context['appointment_images'] = appointment_images
        return context
