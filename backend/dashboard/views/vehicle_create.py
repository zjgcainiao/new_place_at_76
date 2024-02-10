
from .base import CreateView, redirect, messages, reverse_lazy, InternalUserRequiredMixin,timezone,reverse
from dashboard.forms import VehicleCreateForm
from homepageapp.models import VehiclesNewSQL02Model
from django.urls import reverse


class VehicleCreateView(CreateView, InternalUserRequiredMixin):
    model = VehiclesNewSQL02Model
    form_class = VehicleCreateForm
    template_name = 'dashboard/62_vehicle_create.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vehicle_last_updated_at = timezone.now()
        self.object.created_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:vehicle_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('dashboard:vehicle_detail', kwargs={'pk': self.object.pk})