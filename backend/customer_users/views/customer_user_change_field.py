

from .base import render, CustomerUser, redirect
from customer_users.forms import CustomerUserChangeForm
def customer_user_change_field(request):
    if request.method == 'POST':
        form = CustomerUserChangeForm(request.POST)
        if form.is_valid():
            field_name = form.cleaned_data['field_name']
            new_value = form.cleaned_data['new_value']
            instance = request.user  # Assuming the customer user is logged in
            form.save(instance)
            return redirect('customer_user_dashboard')
    else:
        form = CustomerUserChangeForm()

    return render(request, 'customer_user_change_field.html', {'form': form})
