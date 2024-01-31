from .base import LoginRequiredMixin, DetailView, reverse_lazy, get_object_or_404, HttpResponseRedirect,timezone
from homepageapp.models import CustomersNewSQL02Model
from dashboard.forms import CustomerUpdateForm, LiteEmailUpdateForm



class CustomerDetailView(DetailView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    success_url = reverse_lazy('customer-dash')
    context_object_name = 'customer'
    template_name = 'dashboard/41_customer_detail.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomerUpdateForm(
                self.request.POST, instance=self.object)
        else:
            customer = get_object_or_404(
                CustomersNewSQL02Model, pk=self.kwargs['pk'])
            context['email_forms'] = [LiteEmailUpdateForm(
                instance=email) for email in customer.emails.all()]

            context['form'] = CustomerUpdateForm(instance=self.object)
        return context

    def get_queryset(self):

        qs = CustomersNewSQL02Model.objects.prefetch_related(
            'addresses',
            'phones',
            'emails',
            'vehicle_customers').filter(pk=self.kwargs['pk'])
        # qs = qs.filter(repair_order_id=self.kwargs['pk']).get()
        return qs

    def get_success_url(self):
        return reverse('dashboard:customer-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerUpdateForm(request.POST, instance=self.object)

        if form.is_valid():
            self.object.customer_last_updated_at = timezone.now()
            form.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
        # ret911urn self.render_to_response(self.get_context_data(form=form))