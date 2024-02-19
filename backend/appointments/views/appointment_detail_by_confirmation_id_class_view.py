from .base import DetailView, AppointmentImagesForm, get_object_or_404
from .appointment_detail_class_view import AppointmentDetailView






class AppointmentDetailByConfirmationIdView(AppointmentDetailView):
    template_name = 'appointments/30_appointment_detail_by_confirmation_id.html'
    def get_object(self, queryset=None):
        # If no queryset has been provided, use the default queryset for AppointmentRequest
        if queryset is None:
            queryset = self.get_queryset()

        # Use 'appointment_confirmation_id' from URL kwargs to filter the queryset
        appointment_confirmation_id = self.kwargs.get('appointment_confirmation_id')
        
        # Return the object or raise a 404 if not found
        obj = get_object_or_404(queryset, appointment_confirmation_id=appointment_confirmation_id)

        return obj