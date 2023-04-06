# 2023-04-01. ChatGPT 4.0 generated.
# -----------------
from django.conf import settings
from django.shortcuts import render, resolve_url, redirect
import googlemaps
from .forms import AddressForm, InternalUserCreationForm, InternalUserChangeForm
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeDoneView,PasswordChangeView,PasswordResetConfirmView, PasswordContextMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import auth
from django.contrib.auth import authenticate, login
class MyLoginView(LoginView):
    # redirect_authenticated_user = True
    # def get_success_url(self):
    #     return reverse_lazy('dashboard-index')
    # referring to the customized loginv2.html
    # template_name = 'internal_users/loginv2.html'

    template_name = 'internal_users/login.html'
    success_url = reverse_lazy('dashboard')
    
    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()
    
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        return resolve_url(self.next_page or settings.LOGIN_REDIRECT_URL)
    
    # def form_invalid(self, form):
    #     messages.error(self.request, 'Invalid username or password')
    #     return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


## this is the register function to register a new user. 
## necessary validations are needed in the future.

def register(request):
    if request.method == 'POST':
        form = InternalUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = InternalUserCreationForm()
    return render(request, 'internal_users/register.html', {'form': form})

def validate_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = f"{form.cleaned_data['address_line_1']} {form.cleaned_data['address_line_2']}".strip()
            city = form.cleaned_data['city'].strip()
            state = form.cleaned_data['state'].strip()
            zip_code = form.cleaned_data['zip_code'].strip()

            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = gmaps.geocode(f"{address}, {city}, {state} {zip_code}")
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return render(request, 'users/address_validated.html', {'location': location})
            else:
                return render(request, 'users/address_not_found.html')
    else:
        form = AddressForm()

    return render(request, 'users/validate_address.html', {'form': form})



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

