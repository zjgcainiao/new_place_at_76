from django import forms
from customer_users.models import CustomerUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re
from django.core.validators import RegexValidator

# import common functions from common_functions.py
# testing to combine common functions into one centralized location.
from core_operations.common_functions import is_valid_us_phone_number
from core_operations.models import LIST_OF_STATES_IN_US

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox


class CustomerUserRegistrationForm(UserCreationForm):
    cust_user_email = forms.EmailField(help_text='We will important account updates and notifications to this email. Required.', widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', }),label='Email')
    cust_user_phone_number = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder:': 'ex. 213-445-9990 or 2134459990.'}),
        help_text='We will text important updates to this phone number. Optional but recommended.', label='Phone Number')
    cust_user_last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.', label='Last Name',widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }))

        
    cust_user_middle_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.', label='Middle Name')
    
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = CustomerUser
        fields = ['cust_user_email', 'cust_user_phone_number', 'cust_user_first_name','cust_user_middle_name',
                  'cust_user_last_name', 'password1', 'password2']  # 'username',
        # required = ['cust_user_phone_number', 'cust_user_first_name', 'password1', 'password2']
        widgets = {

            'cust_user_first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),

            'password1': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control','placeholder': 'Confirm Password' }),
        }
        labels = {
            'password1': 'Password',
            'password2': 'Repeat Password',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # cust_user_phone_number = forms.CharField(required=True, max_length=20,
    #                                           help_text='enter your phone number. Support US-only numbers. We will not spam you. ')
    # cust_user_email = forms.EmailField(help_text='Enter a valid email address. Recommended.')

    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)


    # Regular expression pattern for valid zip code
    ZIP_CODE_REGEX = r'^\d{5}(?:[-\s]\d{4})?$'
    zip_code_validator = RegexValidator(
        regex=ZIP_CODE_REGEX, message='Enter a valid ZIP code.')

    # format customer_user_first_name
    def clean_cust_user_first_name(self):
        first_name = self.cleaned_data.get('cust_user_first_name').strip()
        if first_name:
            first_name = first_name.capitalize()
        return first_name

    # format customer_user_last_name
    def clean_cust_user_last_name(self):
        last_name = self.cleaned_data.get('cust_user_last_name')
        if last_name:
            last_name = last_name.capitalize()
        return last_name

    def clean_cust_user_phone_number(self):
        phone_number = self.cleaned_data.get('cust_user_phone_number')
        # remove any non-digit input
        phone_number = re.sub(r'\D', '', phone_number)

        if not is_valid_us_phone_number(phone_number):
            raise forms.ValidationError(
                'Please enter a valid US phone number.')
        return phone_number

    # Validate state abbreviation
    def clean_cust_user_address_state(self):
        state = self.cleaned_data.get('cust_user_address_state')
        state = state.upper() if state else None

        if state not in [abbr for abbr, _ in LIST_OF_STATES_IN_US]:
            raise forms.ValidationError(
                'Enter a valid state abbreviation. For example, enter CA for California, TX for Texas. ')
        return state

    # Validate zip code
    def clean_cust_user_address_zip(self):
        zip_code = self.cleaned_data.get('cust_user_address_zip')
        if zip_code:
            self.zip_code_validator(zip_code)
        return zip_code

    def clean_cust_user_email(self):
        email = self.cleaned_data['cust_user_email']
        email = email.strip()
        email = email.lower()
        if email:
            return email
        else:
            raise ValidationError('email cannot be empty.')

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('cust_user_phone_number')
        email = cleaned_data.get('cust_user_email')

        # phone_number = self.clean_phone_number()
        # email = self.clean_email()

        if not phone_number and not email:
            raise forms.ValidationError(
                "Please provide either a phone number or an email address.")
        return cleaned_data

    # save a user by the phone number when this RegistrationForm is saved
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    # this function will have to expand for employee email verifications.
    # a customer user.
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     new = CustomerUser.objects.filter(email=email)
    #     if new.count():
    #         raise ValidationError(" Email Already Exists.")
    #     return email


# the default login requires a phone number and a password
class CustomerUserLoginForm(AuthenticationForm):
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'type': 'text',
    #         'placeholder': 'your phone number',
    #     }),
    #     label='Phone Number',
    # )
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address...',
            'class': 'form-control',
            'type': 'text',
        }),
        label='Email',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'placeholder': 'Enter your password...'
        }),
        label='Password',
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label="Remember Me",
        help_text="Check this box if you want to stay logged in.",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check',
        })
    )


    class Meta:
        model = CustomerUser
        fields=['cust_user_email','password']
        

class CustomerUserChangeForm(forms.Form):
    field_name = forms.CharField(widget=forms.HiddenInput())
    new_value = forms.CharField()

    def save(self, instance):
        field_name = self.cleaned_data['field_name']
        new_value = self.cleaned_data['new_value']

        setattr(instance, field_name, new_value)
        instance.save()


# address validting form
class AddressForm(forms.Form):
    address_line_1 = forms.CharField(max_length=100)
    address_line_2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=10)
    country_code = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        address = f"{cleaned_data['address_line_1']} {cleaned_data['address_line_2']}".strip(
        )
        city = cleaned_data['city'].strip()
        state = cleaned_data['state'].strip()
        zip_code = cleaned_data['zip_code'].strip()
        country_code = cleaned_data['country_code'].strip()

        if not address or not city or not state or not zip_code:
            raise forms.ValidationError("All address fields are required.")

        return cleaned_data
