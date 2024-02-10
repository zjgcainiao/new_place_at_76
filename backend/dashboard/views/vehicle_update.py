from .base import UpdateView, LoginRequiredMixin, redirect, messages, reverse_lazy, timezone
from dashboard.forms import VehicleUpdateForm
from homepageapp.models import VehiclesNewSQL02Model


class VehicleUpdateView(UpdateView, LoginRequiredMixin):
    model = VehiclesNewSQL02Model
    form_class = VehicleUpdateForm
    template_name = 'dashboard/63_vehicle_update.html'
    context_object_name = 'vehicle'
    success_url = reverse_lazy('dashboard:vehicle_detail')
    login_url = reverse_lazy('internal_users:internal_user_login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vehicle_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(
            self.request, f'Vehicle ID: {self.object.pk} update success.')
        return redirect('dashboard:vehicle_detail', pk=self.object.pk)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

