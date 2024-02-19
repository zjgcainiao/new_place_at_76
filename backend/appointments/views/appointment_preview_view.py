from .base import render, get_object_or_404, redirect, APPT_STATUS_SUBMITTED
from appointments.models import AppointmentRequest, AppointmentImages

def appointment_preview_view(request, pk):
    # appointment_id = request.session.get('appointment_id')
    try:
        appointment = get_object_or_404(AppointmentRequest, pk=pk)
        images = AppointmentImages.objects.filter(appointment=appointment)

        # user confirm on the "Confirm" button.

        if request.method == "POST":
            appointment.appointment_status = APPT_STATUS_SUBMITTED
            appointment.save()
            return redirect("appointments:appointment_success_view", pk=appointment.pk)

        context = {'appointment': appointment, 'images': images}
        return render(request, 'appointments/21_appointment_preview.html', context)
    except AppointmentRequest.DoesNotExist:
        # Handle the case where there is no appointment_id in the session
        return redirect('appointments:create_appointment')