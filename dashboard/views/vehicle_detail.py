from .base import DetailView, LoginRequiredMixin, Prefetch, reverse_lazy, HttpResponseRedirect,timezone
from homepageapp.models import VehiclesNewSQL02Model, VehicleNotesModel
from dashboard.forms import VehicleUpdateForm


class VehicleDetailView(DetailView, LoginRequiredMixin):
    model = VehiclesNewSQL02Model
    success_url = reverse_lazy('dashboard:vehicle-dash')
    context_object_name = 'vehicle'
    template_name = 'dashboard/61_vehicle_detail.html'

    def get_queryset(self):
        notes = VehicleNotesModel.objects.filter(vehicle_note_is_active=True)
        return VehiclesNewSQL02Model.objects.prefetch_related(Prefetch('vehiclenotes_vehicle', queryset=notes))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = VehicleUpdateForm(
                self.request.POST, instance=self.object)
        else:
            context['form'] = VehicleUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = VehicleUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            self.object.vehicle_last_updated_at = timezone.now()
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))
