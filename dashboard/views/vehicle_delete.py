from .base import DeleteView, LoginRequiredMixin, redirect, messages, reverse_lazy,InternalUserRequiredMixin
from django.urls import reverse_lazy,reverse
from homepageapp.models import VehiclesNewSQL02Model

class VehicleDeleteView(DeleteView, InternalUserRequiredMixin):

    model = VehiclesNewSQL02Model
    template_name = 'dashboard/64_vehicle_delete.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.vehicle_record_is_active = False  # Soft delete: mark as inactive
        self.object.save()
        messages.success(request, 'vehicle deactivated successfully.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('dashboard:vehicle-dash')