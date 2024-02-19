from .base import DetailView, AppointmentImagesForm
from appointments.models import AppointmentRequest



class AppointmentDetailView(DetailView):
    model = AppointmentRequest
    context_object_name = 'appointment'
    template_name = 'appointments/30_appointment_detail.html'
    # login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentImagesForm()
        return context

    def post(self, request, *args, **kwargs):
        appointment = self.get_object()
        form = AppointmentImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.appointment = appointment
            image.save()
        return self.get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     talent = self.get_object()
    #     form = TalentDocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         document = form.save(commit=False)
    #         document.talent = talent
    #         document.save()
    #     return self.get(request, *args, **kwargs)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)

