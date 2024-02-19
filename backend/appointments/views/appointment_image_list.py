from .base import render, get_object_or_404
from appointments.models import AppointmentRequest, AppointmentImages


def appointment_image_list(request, pk):
    appointment = AppointmentRequest.objects.get(pk=pk)
    images = AppointmentImages.objects.filter(
        image_is_active=True).filter(appointment=appointment).all()
    return render(request, 'appointments/21_appointment_image_list.html', {'images': images, 'appointment': appointment})