from .base import CreateView, LoginRequiredMixin, reverse_lazy, redirect, messages, reverse, timezone
from dashboard.forms import CustomerUpdateForm
from homepageapp.models import CustomersNewSQL02Model

class CustomerCreateView(CreateView, LoginRequiredMixin):
    model = CustomersNewSQL02Model
    form_class = CustomerUpdateForm
    template_name = 'dashboard/42_customer_create.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    # ---- 2023-03-27-------
    # encounter Conversion failed when converting from a character string to uniqueidentifier.
    # ChatGPT 4.0
    # ----------------------
    def form_valid(self, form):
        # Generate a new UUID for the customer_id field. customer_new_uid_v01 -- newly added uuid
        # form.instance.customer_new_uid_v01 = uuid.uuid4()
        # Get the current maximum value of the customer_id field. customer_id is the legacy id used in old DB.
        max_customer_id = CustomersNewSQL02Model.objects.aggregate(Max('customer_id'))[
            'customer_id__max']
        # Increment the max value by 1 to get the new customer_id value
        new_customer_id = max_customer_id + 1 if max_customer_id is not None else 1
        # Set the customer_id value for the new record and save it
        form.instance.customer_id = new_customer_id

        self.object = form.save(commit=False)
        self.object.customer_last_updated_at = timezone.now()
        self.object.modified_by = self.request.user  # assuming the user is logged in
        self.object.save()
        messages.success(self.request, 'Update success.')
        return redirect('dashboard:customer_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('dashboard:customer_detail', kwargs={'pk': self.object.pk})