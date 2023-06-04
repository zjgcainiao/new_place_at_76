from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from customer_users.forms import CustomerUserRegistrationForm, CustomerUserLoginForm
from customer_users.customer_auth_backend import CustomerUserBackend
from customer_users.models import CustomerUser
from formtools.preview import FormPreview

@login_required(login_url='customer_users:customer_user_login')
def dashboard(request):
    # Logic to fetch and display customer-specific dashboard data
    if request.user.is_authenticated and isinstance(request.user, CustomerUser):
        customer_user = request.user
    return render(request, 'customer_users/personal_info.html',{'customer_user': customer_user})


@login_required(login_url='customer_users:customer_user_login')
def personal_information(request):
    # Logic to fetch and display customer's personal information
    return render(request, 'customer_users/personal_information.html')


@login_required(login_url='customer_users:customer_user_login')
def vehicle_list(request):
    # Logic to fetch and display customer's vehicles
    return render(request, 'customer_users/vehicle_list.html')


@login_required(login_url='customer_users:customer_user_login')
def service_history(request, vehicle_id):
    # Logic to fetch and display service history for a specific vehicle
    return render(request, 'customer_users/service_history.html')


def customer_user_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        # two ways to authenticate, use the default authenticate or use the custom one in CustomerUserBackend()
        user = CustomerUserBackend().authenticate(request, phone_number=phone_number, password=password)
        # authenticate via email
        # user = CustomerUserBackend().authenticate_via_email(request, email=email, password=password)
        if user is not None:
            login(request, user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
            return redirect('customer_users:dashboard')
        else:
            # Invalid credentials, handle error
            pass
    return render(request, 'customer_users/customer_user_login.html')

def customer_user_register(request):
    if request.method == 'POST':
        form = CustomerUserRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('cust_user_phone_number')
            # username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = form.save(commit=False)
            user.save()           
            if isinstance(user, CustomerUser):
                customer_user = CustomerUserBackend().authenticate(request, phone_number=phone_number, password=password)
                # Log the user in
                login(request, customer_user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
            else:
                customer_user = None
            # customer_user = CustomerUser.objects.get(cust_user_phone_number=user.cust_user_phone_number)
            # Additional processing, such as creating a customer profile
            # return render('customer_users/customer_user_registration_preview.html', {'form':form})
            return render(request, 'customer_users/customer_user_registration_success.html',{'customer_user':customer_user})
            # return redirect('customer_users:dashboard',{'customer_user': user})
    else:
        form = CustomerUserRegistrationForm()
    return render(request, 'customer_users/customer_user_register.html', {'form': form})


def customer_user_change_field(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        if form.is_valid():
            field_name = form.cleaned_data['field_name']
            new_value = form.cleaned_data['new_value']
            instance = request.user  # Assuming the customer user is logged in
            form.save(instance)
            return redirect('customer_user_dashboard')
    else:
        form = ChangeForm()
    
    return render(request, 'customer_user_change_field.html', {'form': form})