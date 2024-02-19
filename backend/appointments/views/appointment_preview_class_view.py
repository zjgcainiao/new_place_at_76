from .base import FormView, reverse_lazy

class AppointmentPreviewView(FormView):
    template_name = 'appointments/21_appointment_preview.html'
    # form_class = AppointmentCreationForm
    success_url = reverse_lazy('appointments:appointment_success_view')

    def form_valid(self, form):
        self.request.session['appointment_data'] = self.request.POST
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.session.get('appointment_data', {})
        return kwargs
