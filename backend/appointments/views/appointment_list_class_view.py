from appointments.models import AppointmentRequest
from .base import ListView, LoginRequiredMixin, reverse_lazy, APPT_STATUS_CANCELLED
class AppointmentListView(LoginRequiredMixin, ListView):
    model = AppointmentRequest
    context_object_name = 'appointments'
    template_name = 'appointments/20_appointment_list.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_queryset(self):
        # `__` double undestore..more researched are needed.
        qs = AppointmentRequest.objects.prefetch_related(
            'appointment_repair_order').exclude(appointment_status=APPT_STATUS_CANCELLED).all()
        # qs=qs.filter(appointment_status=APPT_STATUS_CANCELLED)
        # select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        # repair order phase defines the WIP (work-in-progress) caegory. 6 means invoice.

        return qs