from .base import get_object_or_404, redirect, messages
from appointments.models import AppointmentImages

def appointment_image_soft_delete(request, image_id):
    image = get_object_or_404(AppointmentImages, image_id=image_id)
    image.image_is_active = False
    image.save()
    messages.add_message(request, messages.WARNING,
                         "The image has been deleted successfully.")
    return redirect('appointment:appointment_image_list')
