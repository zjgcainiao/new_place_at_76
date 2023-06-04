# 2023-04-01. ChatGPT 4.0 generated.
# -----------------
from django.conf import settings
from django.shortcuts import render, resolve_url, redirect
import googlemaps
from internal_users.forms import InternalUserCreationForm, InternalUserChangeForm, InternalUserRegistrationFormV2,InternalUserLoginForm,InternalUserPasswordResetForm
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordContextMixin
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
from internal_users.forms import EmploymentInfoForm
# from internal_users.internal_user_auth_backend import authenticate

## this is the register function to register a new user.
## necessary validations are needed in the future.
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
            user = authenticate(request, email=email, password=password)
            # Log the user in
            # modified on 2023-05-30 added custom InternalUserBackend.
            login(request, user, backend='internal_users.intenral_user_auth_backend.InternalUserBackend')
            # form.save()
            return redirect('dashboard:dashboard-v2')
        # 2023-04-30- added a function to list all error values when there are errors.
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form =  InternalUserRegistrationFormV2()
    return render(request, 'internal_users/10_register.html', {'form': form})

class InternalUserLoginView(LoginView):
    # def get_success_url(self):
    #     return reverse_lazy('dashboard-index')
    # referring to the customized loginv2.html
    # template_name = 'internal_users/loginv2.html'
    template_name = 'internal_users/20_login.html'
    success_url = reverse_lazy('dashboard:dashboard-v2')
    authentication_form = InternalUserLoginForm

    #adding this line will allow users to skip login when the user has been logged in before.
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
        context['title'] = 'Amazing Automan Employee Login'
        return context

class InternalUserLogoutView(LogoutView):
    template_name = 'internal_users/21_logout.html'
    # next_page = reverse_lazy('homepageapp:homepage')
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'internal_users/password_change.html'
    success_url = reverse_lazy('password_change_done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='internal_users/password_change_done.html'


# 'PasswordResetView" class Allows a user to reset their password by generating a one-time use link that 
# can be used to reset the password, and sending that link to the user’s registered email address.
class UserPasswordResetView(PasswordResetView):
    template_name = 'internal_users/30_password_reset.html'

    success_url = reverse_lazy('password_reset_confirm')  #'/password_reset/done/'

    form_class=InternalUserPasswordResetForm
    email_template_name = 'internal_users/password_reset_email.html'
    subject_template_name = 'internal_users/password_reset_subject.txt'

    def form_valid(self, form):
        InternalUserModel = get_user_model()
        email = form.cleaned_data['email'].lower()
        users = InternalUserModel.objects.filter(user_is_active=True, email__iexact=email)
        if not users.exists():
            return self.form_valid(form)
        return super().form_valid(form)



# ---- 2023-04-03 creating firebase authentication view funciton ----
# in the firebase_auth.py, create a new class `authentication.BaseAuthentication`
@login_required
def firebase_authenticate(request):
    if request.method == 'GET':
        form = InternalUserCreationForm()
        return render(request, 'internal_users/register.html', {'form': form})
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
        django_user = authenticate(request, username=user.email, password='password')

        if django_user is not None:
            login(request, django_user)
            return redirect('dashboard',{'logged_in_customized_user': django_user})
        else:
            raise Exception('Failed to authenticate user')

        # except Exception as e:
        #     return render(request, 'internal_users/pages-404.html', {'error': str(e)})

def InternalUserDashboard(request):
    if isinstance(request.user, InternalUser) and request.user.is_authenticated:
        internal_user = request.user
        return render(request, 'internal_users/60_internal_user_dashboard.html', {'internal_user': internal_user})
    else:
        render

def internal_user_view_employement(request):
    if isinstance(request.user, InternalUser) and request.user.is_authenticated:
        internal_user = request.user
        email = internal_user.email
        # grab the talent record based on email
        # next step is allow user to enter the birthday so that he can confirm the real employee information before displaying it.
        talent = TalentsModel.objects.filter(talent_email="15@gmail.com")
        # if talent.exists():
        talent_instance = talent.get()
        form = EmploymentInfoForm(instance=talent_instance)
        # crispy_form = render_crispy_form(form)
        # qs = RepairOrdersNewSQL02Model.objects.select_related('repair_order_customer').prefetch_related('repair_order_customer__addresses')
        return render(request, 'internal_users/70_employment_information.html', {"talent": talent_instance, "form": form})