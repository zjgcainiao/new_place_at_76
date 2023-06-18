from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from customer_users.forms import CustomerUserRegistrationForm, CustomerUserLoginForm
from customer_users.customer_auth_backend import CustomerUserBackend
from customer_users.models import CustomerUser
from formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from customer_users.tasks import create_customer_user_from_firebase_auth, create_firebase_auth_user
from firebase_auth_app.models import FirebaseUser
import json 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib import messages

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
            return render(request, 'customer_users/60_customer_user_registration_success.html',{'customer_user':customer_user})
            # return redirect('customer_users:dashboard',{'customer_user': user})
    else:
        form = CustomerUserRegistrationForm()
    return render(request, 'customer_users/10_customer_user_register.html', {'form': form})


@login_required(login_url='customer_users:customer_user_login')
def customer_user_dashboard(request):
    # Logic to fetch and display customer-specific dashboard data
    if request.user.is_authenticated and isinstance(request.user, CustomerUser):
        # customer_user = request.user
        customer_user = CustomerUser.objects.get(cust_user_id=request.user.cust_user_id)
    return render(request, 'customer_users/80_customer_user_dashboard.html',{'customer_user': customer_user})
    # return render(request, 'customer_users/51_dashboard_personal_info.html',{'customer_user': customer_user})
    
def customer_user_login(request):
    if request.method == 'POST':
        # phone_number = request.POST['phone_number']
        email = request.POST['username']
        password = request.POST['password']
        form = CustomerUserLoginForm(request.POST)
        # two ways to authenticate, use the default authenticate or use the custom one in CustomerUserBackend()
        # if phone_number is None or len(phone_number)==0:
        user = CustomerUserBackend().authenticate_via_email(request, email=email, password=password)
        # authenticate via email
        # user = CustomerUserBackend().authenticate_via_email(request, email=email, password=password)
        if user is not None:
            login(request, user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
            return redirect('customer_users:customer_user_dashboard')
        else:
            # Invalid credentials, handle error
            pass
    else:
        form = CustomerUserLoginForm()
        # if isinstance(request.user, CustomerUser):
        #     redirect('customer_users:customer_user_dashboard')
    return render(request, 'customer_users/20_customer_user_login.html', {'form': form})



@login_required
def customer_user_logout(request):
    messages.info(request, "Hi %s, you have been signed out." % request.user.cust_user_email)
    logout(request)
    return redirect('homepageapp:homepage')
    # return redirect('login') 


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


def customer_user_registration_success(request):
    if isinstance(request.user, CustomerUser):
        customer_user = request.user
    else:
        customer_user = None
    return render(request, 'customer_users/60_customer_user_registration_success.html',{'customer_user':customer_user})


def customer_user_register_firebaseauth(request):
    return render(request, 'customer_users/11_customer_user_register_with_firebaseauth.html')

def customer_user_login_firebaseauth(request):
    return render(request, 'customer_users/21_customer_user_login_with_firebaseauth.html')

def firebase_auth_signin_precheck(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        uid = data.get('uid')
        redirect_url = reverse_lazy('customer_users:customer_user_dashboard')
        try:
            customer_user = CustomerUser.objects.get(cust_user_email=email)  # check if the user exists
            print(customer_user)
            if customer_user is not None:
                login(request, customer_user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
            # return redirect('customer_users:customer_user_dashboard')
            return JsonResponse({"status": "OK", "redirect_url": redirect_url}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create the user
            create_customer_user_from_firebase_auth.delay(uid, email)
            return JsonResponse({"status": "OK", "message": "User does not exist. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)
    
@csrf_exempt
# @login_required(login_url='customer_users:customer_user_login')
def firebase_auth_user_creation(request):
    if request.method == 'POST':
        # if isinstance(request.user, CustomerUser):
        #     request.user.
        data = json.loads(request.body)
        firebase_user_uid = data.get('uid')
        firebase_user_email = data.get('email')
        firebase_user_display_name = data.get('display_name')
        # firebase_user_phone_number = request.POST.get('')
        firebase_user_password = data.get('password')

        # the password shall not be inlcuded in the FirebaseUser model. Use firebase auth to handle authentication.
        # FirebaseUser model 
        try:
            firebase_user = FirebaseUser.objects.get(firebase_user_email=firebase_user_email)
            firebase_user.firebase_user_display_name = firebase_user_display_name 
            firebase_user.firebase_user_uid = firebase_user_uid
            firebase_user.save()
            create_customer_user_from_firebase_auth.delay(firebase_user.uuid, firebase_user_password)
            request.user = CustomerUser.objects.get(cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "User exists."}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create a record of FirebaseUser
            # then creating a symbolic customer_user instance that links to the new firebaseuser.
            # firebase_user_task = 
            create_firebase_auth_user.delay(firebase_user_uid, firebase_user_email, firebase_user_display_name, firebase_user_password)
            
            # firebase_user = firebase_user_task.get()
            # if firebase_user is not None:
            #     create_customer_user_from_firebase_auth.delay(firebase_user.uuid, firebase_user_email,firebase_user_password)
            
            # request.user = CustomerUser.objects.get(cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "First Time firebase user. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)
    

## this function is NOT finished. 
# 2023-06-12
@csrf_exempt
def sign_up_via_gmail_to_backend(request):
    if request.method == 'POST':
        # if isinstance(request.user, CustomerUser):
        #     request.user.
        data = json.loads(request.body)
        firebase_user_uid = data.get('uid')
        firebase_user_email = data.get('email')
        firebase_user_display_name = data.get('display_name')
        firebase_user_token = request.POST.get('token')
        firebase_user_credential = data.get('credential')
        firebase_user = {
            'uid':firebase_user_uid,
            'email':firebase_user_email,
            'display_name': firebase_user_display_name,
            'token': firebase_user_token,
            'credential':firebase_user_credential
        }
        return render(request, 'customer_users/60_customer_user_registration_success_via_gmail.html', firebase_user)
    
@login_required(login_url='customer_users:customer_user_login')
def get_personal_info(request):
    # implement your logic here to get personal info
    if isinstance(request.user, CustomerUser) and request.method=='GET':
        customer_user = request.user
    return render(request, 'customer_users/82_dashboard_personal_info_v2.html', {'customer_user':customer_user})

@login_required(login_url='customer_users:customer_user_login')
def get_my_vehicles(request):
    # implement your logic here to get vehicle info
    data = {'vehicles': ['Car 1', 'Car 2', 'Car 3']}
    return JsonResponse(data)


@login_required(login_url='customer_users:customer_user_login')
def get_service_history(request, vehicle_id):
    # Logic to fetch and display service history for a specific vehicle
    return render(request, 'customer_users/service_history.html')
