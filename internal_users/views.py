# 2023-04-01. ChatGPT 4.0 generated.
# -----------------
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponseForbidden
from internal_users.forms import InternalUserCreationForm, InternalUserChangeForm, InternalUserRegistrationFormV2, InternalUserLoginForm, InternalUserPasswordResetForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordContextMixin
from internal_users.models import InternalUser
from talent_management.models import TalentsModel
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from crispy_forms.utils import render_crispy_form
from internal_users.forms import EmploymentInfoForm, InternalUserPasswordChangeForm
from internal_users.internal_user_auth_backend import InternalUserBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import Group
from internal_users.token_generators import account_activation_token, decode_activation_token
import logging
# from internal_users.internal_user_auth_backend import authenticate
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from internal_users.mixins import InternalUserRequiredMixin


logger = logging.getLogger('django')

# this is the register function to register a new user.
# necessary validations are needed in the future.


def register(request):
    if request.method == 'POST':
        # form = InternalUserCreationForm(request.POST)
        # version 2 of registeration -- via InternalUserRegistrationFormV2
        form = InternalUserRegistrationFormV2(request.POST)
        if form.is_valid():
            # Save the user's information
            user = form.save(commit=False)
            # form.save()
            user.user_first_name = form.cleaned_data.get('first_name')
            user.user_last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email').lower()
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            email = form.cleaned_data.get('email')
            # username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # raw_password = form.cleaned_data.get('password1')
            user = InternalUserBackend().authenticate(
                request, email=email, password=password)
            # Log the user in
            # modified on 2023-05-30 added custom InternalUserBackend.
            login(
                request, user, backend='internal_users.intenral_user_auth_backend.InternalUserBackend')
            # form.save()
            return redirect('dashboard:main-dash')
        # 2023-04-30- added a function to list all error values when there are errors.
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = InternalUserRegistrationFormV2()
    return render(request, 'internal_users/10_register.html', {'form': form})


class InternalUserLoginView(LoginView):

    # template_name = 'internal_users/loginv2.html'
    template_name = 'internal_users/20_login.html'
    success_url = reverse_lazy('dashboard:repair-order-dash')
    authentication_form = InternalUserLoginForm

    # adding this line will allow users to skip login when the user has been logged in before.
    # it does add complexity on my debugging; use private mode in a browser.
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     return self.get_redirect_url() or self.get_default_redirect_url()

    # def get_default_redirect_url(self):
    #     """Return the default redirect URL."""
    #     return resolve_url(self.next_page or settings.LOGIN_REDIRECT_URL)

    # def form_invalid(self, form):
    #     messages.error(self.request, 'Invalid username or password')
    #     return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Login'
        return context


def internal_user_login(request):
    if request.method == 'POST':
        # phone_number = request.POST['phone_number']
        email = request.POST.get('username').lower().strip()
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        form = InternalUserLoginForm(request.POST)
        # two ways to authenticate, use the default authenticate or use the custom one in CustomerUserBackend()
        # if phone_number is None or len(phone_number)==0:
        # user = InternalUserLoginForm().authenticate_via_email(request, email=email, password=password)
        # authenticate via email
        user = InternalUserBackend().authenticate(
            request, email=email, password=password)
        if user is not None:
            login(
                request, user, backend='internal_users.internal_user_auth_backend.InternalUserBackend')
            if not remember_me:  # if 'remember_me' box is not checked, then set the session to expire when the user closes the browser.
                request.session.set_expiry(60*60*24*14) # 14 days
            return redirect('internal_users:internal_user_dashboard')
        else:
            # Invalid credentials, handle error
            messages.error(request, "Invalid email or password.")
            pass
    else:
        form = InternalUserLoginForm()
        # if isinstance(request.user, CustomerUser):
        #     redirect('customer_users:customer_user_dashboard')
    return render(request, 'internal_users/20_login.html', {'form': form})


class InternalUserLogoutView(LogoutView):
    template_name = 'internal_users/21_logout.html'
    next_page = reverse_lazy('homepageapp:homepage')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

# @login_required(login_url='internal_users:internal_user_login')


class InternalUserPasswordChangeView(PasswordChangeView):
    template_name = 'internal_users/40_password_change.html'
    # form_class = InternalUserPasswordChangeForm
    success_url = reverse_lazy('internal_users:password_change_done')


class InternalUserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'internal_users/41_password_change_done.html'


# 'PasswordResetView" class Allows a user to reset their password by generating a one-time use link that
# can be used to reset the password, and sending that link to the user’s registered email address.
class InternalUserPasswordResetView(PasswordResetView):
    template_name = 'internal_users/30_password_reset.html'

    # '/password_reset/done/'
    success_url = reverse_lazy('internal_users:password_reset_confirm')

    form_class = InternalUserPasswordResetForm
    email_template_name = 'internal_users/34_password_reset_email.html'
    subject_template_name = 'internal_users/35_password_reset_subject.txt'

    def form_valid(self, form):
        InternalUserModel = get_user_model()
        email = form.cleaned_data['email'].lower()
        users = InternalUserModel.objects.filter(
            user_is_active=True, email__iexact=email)
        if not users.exists():
            return self.form_valid(form)
        return super().form_valid(form)


# ---- 2023-04-03 creating firebase authentication view funciton ----
# in the firebase_auth.py, create a new class `authentication.BaseAuthentication`
@login_required(login_url='internal_users:internal_user_login')
def firebase_authenticate(request):
    if request.method == 'GET':
        form = InternalUserCreationForm()
        return render(request, 'internal_users/10_register.html', {'form': form})
    else:

        # if request.method is `POST`
        # Get the Firebase ID token from the request
        firebase_id_token = request.POST.get('firebase_id_token', '')

        # try:
        # Verify the Firebase ID token

        decoded_token = auth.verify_id_token(firebase_id_token)
        uid = decoded_token['uid']
        # uid='J58ELAzoSIWanLfmaFDF22RuKBT2'

        # Get the user object from Firebase Authentication
        user = auth.get_user(uid)

        # Authenticate the user in Django
        django_user = authenticate(
            request, username=user.email, password='password')

        if django_user is not None:
            login(request, django_user)
            return redirect('dashboard', {'logged_in_customized_user': django_user})
        else:
            raise Exception('Failed to authenticate user')

        # except Exception as e:
        #     return render(request, 'internal_users/pages-404.html', {'error': str(e)})


@login_required(login_url='internal_users:internal_user_login')
def fetch_internal_user_dashboard(request):
    if isinstance(request.user, InternalUser) and request.user.is_authenticated:
        internal_user = request.user
        return render(request, 'internal_users/60_internal_user_dashboard.html', {'user': internal_user})
    else:
        messages.error(
            f'the current user does not have sufficient access to the page. Our employees need to login in.')
        return reverse_lazy('internal_users:internal_user_login')

# currently used to return the user's dashboard, aka the profile page.
class UserInfoView(TemplateView, InternalUserRequiredMixin):

    template_name = 'internal_users/72_internal_user_view_user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request.user
        return context


@login_required(login_url='internal_users:internal_user_login')
def internal_user_view_employement(request):
    if isinstance(request.user, InternalUser) and request.user.is_authenticated:
        internal_user = request.user
        email = internal_user.email
        # grab the talent record based on email
        # next step is allow user to enter the birthday so that he can confirm the real employee information before displaying it.
        talent = TalentsModel.objects.filter(
            talent_email=email)
        if talent.exists():
            talent_instance = talent.get()
            form = EmploymentInfoForm(instance=talent_instance)
            # crispy_form = render_crispy_form(form)
            # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
            return render(request, 'internal_users/70_employment_information.html', {"talent": talent_instance, "form": form})
        else:
            return HttpResponseForbidden('No talent found with the given email.')
    else:
        messages.error('you are not authorized to view this page.')
        return redirect('homepageapp:homepage')


# @login_required(login_url='internal_users:internal_user_login')
def return_current_internal_user_json(request):
    data = {
        'is_authenticated_user': request.user.is_authenticated,
        'is_internal_user': isinstance(request.user, InternalUser),
    }

    # Add other user details as needed
    if request.user.is_authenticated:
        data['email'] = request.user.email
        # Check if user belongs to 'Technicians' group
        data['is_technician'] = True  # manual setting for testing purpose
        # Group.objects.get(
        #    name='Technicians') in request.user.groups.all()
    else:
        data['email'] = None
        data['is_technician'] = False

    return JsonResponse(data)


def activate_internal_user_account(request, token):
    logger.info(f' the JWT token received from activation link is {token}')
    try:
        decoded_payload = decode_activation_token(token)
        if decoded_payload:
            logger.info(f'decoding user token scuccessfull')
            user_id = decoded_payload['user_id']
            logger.info(f'the decoded user_id is {user_id or None}')
            user = InternalUser.objects.get(pk=user_id)
            user.user_is_active = True
            user.save()
            messages.success(
                f'user {user.user_first_name} (ID: {user.pk}) activation was successful.')
            return redirect('internal_users:internal_user_dashboard')
    except (TypeError, ValueError, OverflowError, InternalUser.DoesNotExist):
        user = None
        logger.info(
            f'activating user {user.user_first_name} (ID: {user.pk}) was unsuccessful. ')
        return render(request, 'internal_users/11_activation_invalid.html')

