from .base import LoginRequiredMixin, DeleteView, redirect, messages, reverse_lazy
from homepageapp.models import CustomersNewSQL02Model



class CustomerDeleteView(DeleteView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    template_name = 'dashboard/44_customer_delete.html'
    # Redirect to customer list after "deletion"
    success_url = reverse_lazy('dashboard:customer_dash')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.customer_is_deleted = True  # Soft delete: mark as inactive
        self.object.customer_is_active = False  # Soft delete: mark as inactive
        self.object.save()
        messages.success(request, 'Customer deactivated successfully.')
        return redirect(self.get_success_url())