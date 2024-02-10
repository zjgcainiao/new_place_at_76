from .base import LoginRequiredMixin, DetailView, get_object_or_404, redirect, messages
from homepageapp.models import CustomersNewSQL02Model, EmailsNewSQL02Model, CustomerEmailsNewSQL02Model
from dashboard.forms import LiteEmailUpdateForm

def update_customer_email(request, email_id):
    # email_id = request.POST.get('email_id')
    email = get_object_or_404(EmailsNewSQL02Model, pk=email_id)

    customer_email_relation = CustomerEmailsNewSQL02Model.objects.filter(
        email=email).first()

    if not customer_email_relation:
        messages.error(request, "No customer associated with this email.")
        # Redirect to some default page or handle this error appropriately
        return redirect('default_page')

    customer_id = customer_email_relation.customer.pk

    if request.method == "POST":
        form = LiteEmailUpdateForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            messages.success(request, "Email has been updated successfully.")
            return redirect('dashboard:customer_detail', pk=customer_id)
            # return JsonResponse({'status': 'success'})
        else:
            messages.error(
                request, "Error updating the email. Please try again.")
            # error_json = JsonResponse(
            #     {'status': 'error', 'errors': form.errors})
            # context = {"pk": customer_id, 'error_json_response': error_json}
            return redirect('dashboard:customer_detail', pk=customer_id) 