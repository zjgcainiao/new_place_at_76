
from .base import render, CustomerUserLoginForm, CustomerUserBackend, login, redirect, logging, messages




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
            
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f'getting the login email for customer user: {email}')
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
