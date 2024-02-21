from .base import render, CustomerUserRegistrationForm, CustomerUser

def customer_user_register(request):
    if request.method == 'POST':
        form = CustomerUserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('cust_user_email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('cust_user_first_name')
            last_name = form.cleaned_data.get('cust_user_last_name')
            middle_name = form.cleaned_data.get('cust_user_middle_name')
            phone_number = form.cleaned_data.get('cust_user_phone_number')
            print(
                f'here is the password used to creating this customer email {email}:{password}....')
            # Use the create_user method to create a new customer user. The proper way
            customer_user = CustomerUser.objects.create_user(email=email, password=password)
            # saving the rest of info
            if first_name or last_name or middle_name or phone_number:
                customer_user.cust_user_first_name = first_name
                customer_user.cust_user_last_name = last_name
                customer_user.cust_user_middle_name = middle_name
                customer_user.cust_user_phone_number = phone_number

            customer_user.save()

            print(f'saving the new customer user {customer_user.pk}...')
            return render(request, 'customer_users/60_customer_user_registration_success.html', {'customer_user': customer_user})
    else:
        form = CustomerUserRegistrationForm()
    return render(request, 'customer_users/10_customer_user_register.html', {'form': form})