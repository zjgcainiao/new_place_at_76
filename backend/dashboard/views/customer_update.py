
from .base import LoginRequiredMixin, UpdateView, redirect, messages, reverse_lazy, reverse, timezone
from dashboard.forms import CustomerUpdateForm, AddressFormset, EmailFormset, PhoneFormset
from dashboard.forms import AddressFormset, EmailFormset, PhoneFormset
from homepageapp.models import CustomersNewSQL02Model

class CustomerUpdateView(UpdateView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    form_class = CustomerUpdateForm
    template_name = 'dashboard/43_customer_update.html'
    success_url = reverse_lazy('dashboard:customer_detail')
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            customer = self.get_object()
            context['addresses_formset'] = AddressFormset(
                self.request.POST, instance=self.object)
            context['emails_formset'] = EmailFormset(
                self.request.POST, instance=self.object)
            context['phones_formset'] = PhoneFormset(
                self.request.POST, instance=self.object)
        else:
            context['addresses_formset'] = AddressFormset(
                instance=self.object)
            context['emails_formset'] = EmailFormset(instance=self.object)
            context['phones_formset'] = PhoneFormset(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:customer_detail', pk=self.object.customer_id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
