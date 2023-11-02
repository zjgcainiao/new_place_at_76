import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from customer_users.forms import CustomerUserRegistrationForm, CustomerUserLoginForm
from customer_users.customer_auth_backend import CustomerUserBackend
from customer_users.models import CustomerUser
from formtools.preview import FormPreview
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from firebase_admin import auth
from customer_users.tasks import create_customer_user_from_firebase_auth, create_firebase_auth_user
from firebase_auth_app.models import FirebaseUser
from asgiref.sync import sync_to_async
from dashboard.async_functions import database_sync_to_async

from customer_users.token_generators import decode_activation_token_for_customer_user, create_activation_token_for_customer_user


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
            customer_user = CustomerUser.objects.create_user(
                email=email, password=password)
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


# 2023-10-13 added to require a email verification:
# prefer built-in login over FirebaseAuth login at this moment.

def activate_customer_user_account(request, token):

    logger = logging.getLogger('django.request')

    logger.info(f' the JWT token received from activation link is {token}')
    print(f'new customer user token recieved: {token}')
    try:
        decoded_payload = decode_activation_token_for_customer_user(token)

        if not decoded_payload:
            messages.error(
                request, f'Account activation failure. Invalid or Expired Token.')
            return redirect('customer_users:customer_user_login')

        user_id = decoded_payload['user_id']
        email_verified = decoded_payload['email_verified']
        user = CustomerUser.objects.get(pk=user_id)

        logger.info(f'Decoding user token scuccessfull.')
        # print(f'Decoding customer user token scuccessfull.')
        user_id = decoded_payload['user_id']
        email_verified = decoded_payload['email_verified']
        # print(f'email_verified  decoded: {email_verified}')
        # print(f'user_id decoded: {user_id}')
        print(f'current email_verified: {user.cust_user_email_verified}')

        logger.info(f'the decoded user_id is {user_id or None}')
        user = CustomerUser.objects.get(pk=user_id)
        # If email was not verified at the time of token creation, verify now
        if not email_verified and not user.cust_user_email_verified:
            user.cust_user_email_verified = True
            user.save()
            logger.info(f'Activating customer user {user.pk}...')
            print(f'Activating customer user {user.pk}...')
            # url=redirect('customer_users:customer_user_login')
            # print(f'redirecting url is {url}.....new email_verified: {user.cust_user_email_verified}')
            messages.success(
                request, f'Account activation was successful. Thank you for your efforts. You can login now.')
            return redirect('customer_users:customer_user_login')
        elif not email_verified and user.cust_user_email_verified:
            messages.SUCCESS(
                request, f'Account {user.pk} had been activated. Email verified.')
            return redirect('customer_users:customer_user_login')
        else:
            messages.error(request, 'error activating account...')
            return redirect('customer_users:customer_user_login')

    except (TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
        user = None
        logger.info(
            f'activating customer user was unsuccessful.')
        return render(request, 'customer_users/11_customer_user_activation_invalid.html')


def customer_user_login(request):
    # Customer User Login Form
    # form = CustomerUserLoginForm()
    logger = logging.getLogger('django.request')
    # print('running customer_user_login view function...')
    if request.method == 'POST':
        # print('login form posted.')
        # phone_number = request.POST['phone_number']
        # email = request.POST['username']
        # password = request.POST['password']
        # print(
        #     f'any email from request.POST["username"].. {request.POST["username"]}')
        form = CustomerUserLoginForm(request.POST)
        # two ways to authenticate, use the default authenticate or use the custom one in CustomerUserBackend()
        # if phone_number is None or len(phone_number)==0:
        print(
            f'customer_user login form submitted...form_valid() status: {form.is_valid()}...')
        # print(f'form in request.POST is {request.POST["form"]}...')
        # print(f'{form}')
        if form.is_valid():
            print(f'getting the login email for customer user: {email}')
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate customer_user
            user = CustomerUserBackend().authenticate(
                request, email=email, password=password)
            print(
                f'authenticating customer user {email} successful.logging in now...')
            if user:
                login(
                    request, user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
                return redirect('customer_users:get_personal_info')
            else:
                # Invalid credentials, handle error
                logger.error(
                    f'customer user login error detected. user email entered {email}')
                messages.error(
                    request, 'cannot authenticate the email and password combo.')
        else:
            print(f'here are the form error(s): {form.errors}')
            messages.error(
                request, f'There seems to be an error in the form. Please check your inputs. {form.errors}')
            # pass
            email = request.POST['username']
            password = request.POST['password']
            # Authenticate customer_user
            user = CustomerUserBackend().authenticate(
                request, email=email, password=password)
            print(
                f'authenticating customer user {email} successful.logging in now...')
            if user:
                login(
                    request, user, backend='customer_users.customer_auth_backend.CustomerUserBackend')
                return redirect('customer_users:get_personal_info')
            else:
                # Invalid credentials, handle error
                logger.error(
                    f'customer user login error detected. user email entered {email}')
                messages.error(
                    request, 'cannot authenticate the email and password combo.')
    else:
        form = CustomerUserLoginForm()
        # if isinstance(request.user, CustomerUser):
        #     redirect('customer_users:customer_user_dashboard')
    return render(request, 'customer_users/12_customer_user_login.html', {'form': form})


def customer_user_profile(request):
    customer_user = None
    # Logic to fetch and display customer-specific dashboard data
    if request.user.is_authenticated and isinstance(request.user, CustomerUser):
        print(f'the user type is {isinstance(request.user, CustomerUser)}')
        # customer_user = request.user
        customer_user = CustomerUser.objects.get(
            pk=request.user.cust_user_id)
        if customer_user.cust_user_email_verified:
            return render(request, 'customer_users/20_customer_user_profile.html', {'customer_user': customer_user})
        else:
            return render(request, 'customer_users/20_customer_user_profile.html', {'customer_user': customer_user})
    else:
        print(
            f'The user type {request.user}is customerUser?:{isinstance(request.user, CustomerUser)}')
        return redirect('customer_users:customer_user_login')

    # return render(request, 'customer_users/51_dashboard_personal_info.html',{'customer_user': customer_user})


def customer_user_profile_new(request):
    customer_user = None
    # Logic to fetch and display customer-specific dashboard data
    if request.user.is_authenticated and isinstance(request.user, CustomerUser):
        print(f'the user type is {isinstance(request.user, CustomerUser)}')
        # customer_user = request.user
        customer_user = CustomerUser.objects.get(
            pk=request.user.cust_user_id)
        if customer_user.cust_user_email_verified:
            return render(request, 'customer_users/20_customer_user_profile_new.html', {'customer_user': customer_user})
        else:
            return render(request, 'customer_users/20_customer_user_profile_new.html', {'customer_user': customer_user})
    else:
        print(
            f'The user type {request.user}is customerUser?:{isinstance(request.user, CustomerUser)}')
        messages.error(
            request, f'you are not authorized to view this page. please login first or try it again.')
        return redirect('customer_users:customer_user_login')

    # return render(request, 'customer_users/51_dashboard_personal_info.html',{'customer_user': customer_user})


def customer_user_logout(request):
    messages.info(request,
                  f"Hi {request.user.cust_user_email}, you have been signed out.")
    logout(request)
    return redirect('homepageapp:homepage')


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
    return render(request, 'customer_users/60_customer_user_registration_success.html', {'customer_user': customer_user})

# only renders the html templates


def customer_user_register_firebaseauth(request):
    return render(request, 'customer_users/11_customer_user_register_with_firebaseauth.html')


def customer_user_login_firebaseauth(request):
    return render(request, 'customer_users/13_customer_user_login_with_firebaseauth.html')


def firebase_auth_signin_precheck(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        uid = data.get('uid')
        redirect_url = reverse_lazy('customer_users:customer_user_dashboard')
        try:
            customer_user = CustomerUser.objects.get(
                cust_user_email=email)  # check if the user exists
            print(customer_user)
            if customer_user is not None:
                login(request, customer_user,
                      backend='customer_users.customer_auth_backend.CustomerUserBackend')
            # return redirect('customer_users:customer_user_dashboard')
            return JsonResponse({"status": "OK", "redirect_url": redirect_url}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create the user
            create_customer_user_from_firebase_auth.delay(uid, email)
            return JsonResponse({"status": "OK", "message": "User does not exist. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)


# @csrf_exempt
# @login_required(login_url='customer_users:customer_user_login')
def firebase_auth_user_creation(request):
    if request.method == 'POST':
        # if isinstance(request.user, CustomerUser):
        #     request.user.
        data = json.loads(request.body)

        firebase_user_uid = data.get('uid')
        print(f'firebase user uid is {firebase_user_uid}')
        firebase_user_email = data.get('email')
        firebase_user_display_name = data.get('display_name')
        # firebase_user_phone_number = request.POST.get('')
        firebase_user_password = data.get('password')

        # the password shall not be inlcuded in the FirebaseUser model. Use firebase auth to handle authentication.
        # FirebaseUser model
        try:
            firebase_user = FirebaseUser.objects.get(
                firebase_user_email=firebase_user_email)
            firebase_user.firebase_user_display_name = firebase_user_display_name
            firebase_user.firebase_user_uid = firebase_user_uid
            firebase_user.save()
            # create_customer_user_from_firebase_auth.delay(
            #     firebase_user.uuid, firebase_user_password)
            create_customer_user_from_firebase_auth(
                firebase_user.firebase_user_id, firebase_user_password)
            request.user = CustomerUser.objects.get(
                cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "User exists."}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create a record of FirebaseUser
            # then creating a symbolic customer_user instance that links to the new firebaseuser.

            # this is an async way to call the task when celery is available
            # create_firebase_auth_user.delay(
            #     firebase_user_uid, firebase_user_email, firebase_user_display_name, firebase_user_password)
            create_firebase_auth_user(
                firebase_user_uid, firebase_user_email, firebase_user_display_name, firebase_user_password)

            # firebase_user = firebase_user_task.get()
            # if firebase_user is not None:
            #     create_customer_user_from_firebase_auth.delay(firebase_user.uuid, firebase_user_email,firebase_user_password)

            # request.user = CustomerUser.objects.get(cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "First Time firebase user. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)


# this function is NOT finished.
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
            'uid': firebase_user_uid,
            'email': firebase_user_email,
            'display_name': firebase_user_display_name,
            'token': firebase_user_token,
            'credential': firebase_user_credential
        }
        return render(request, 'customer_users/60_customer_user_registration_success_via_gmail.html', firebase_user)


@login_required(login_url='customer_users:customer_user_login')
def get_vehicle_search_page(request):
    # implement your logic here to get vehicle info
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_search_vin.html', {'customer_user': customer_user})


@login_required(login_url='customer_users:customer_user_login')
def get_personal_info(request):
    # implement your logic here to get personal info
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_personal_info.html', {'customer_user': customer_user})


@login_required(login_url='customer_users:customer_user_login')
def get_personal_info_v2(request):
    # implement your logic here to get personal info
    if isinstance(request.user, CustomerUser) and request.method == 'GET':
        customer_user = request.user
    return render(request, 'customer_users/30_profile_personal_info_v2.html', {'customer_user': customer_user})


@login_required(login_url='customer_users:customer_user_login')
def get_my_vehicles(request):
    # implement your logic here to get vehicle info
    data = {'vehicles': ['Car 1', 'Car 2', 'Car 3']}
    return JsonResponse(data)


@login_required(login_url='customer_users:customer_user_login')
def get_service_history(request, vehicle_id):
    # Logic to fetch and display service history for a specific vehicle
    return render(request, 'customer_users/service_history.html')

# 2023-10-13
# defined to verify a token from authenticated user via firebase auth javscript script.
# the script is defined in firebase_auth_register_and_sign_in_with_django.js that is serverd via static files via "{% static '' %}"


async def verify_token(request):
    token = request.POST.get('token')
    user_data = request.POST.get('user_data')
    new_user_flag = request.POST.get('newUserFlag')

    # Verify Firebase token
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
    except:
        return JsonResponse({'success': False, 'error': 'Invalid token'})

    # added variable to check if the token verification is for login or registration.
    if new_user_flag:
        firebase_user = await sync_to_async(FirebaseUser.objects.create,
                                            thread_sensitive=True)(firebase_user_uid=uid, defaults=user_data)

    else:
        firebase_user = await sync_to_async(FirebaseUser.objects.get,
                                            thread_sensitive=True)(firebase_user_uid=uid)

    if firebase_user:
        # You can set additional user fields here if needed
        pass
    login(request, firebase_user)

    return JsonResponse({'success': True})
