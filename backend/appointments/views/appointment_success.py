from .base import render, get_object_or_404
from appointments.models import AppointmentRequest, AppointmentImages

def appointment_success(request, pk):
    appointment = get_object_or_404(AppointmentRequest, pk=pk)
    context = {'appointment': appointment}
    return render(request, 'appointments/22_appointment_creation_success.html', context)