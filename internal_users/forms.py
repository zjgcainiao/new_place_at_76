# 2023-04-01 chatGPT generated form ---

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import InternalUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from talent_management.models import TalentsModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox


class InternalUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = InternalUser
        fields = ('user_id', 'email', 'user_first_name', 'user_last_name',
                  )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# version 2 --- via UserCreationForm, AuthenticationForm
# 2023-04-26-chat-GPT-enabled


class InternalUserRegistrationFormV2(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text='Required. Enter a valid email address.')
    user_first_name = forms.CharField(
        max_length=50, required=True, help_text='Required.')
    user_last_name = forms.CharField(
        max_length=50, required=True, help_text='Required.')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    # this function will have to expand for employee email verifications.
    # employee record shall be created first before a user can be added.

    def email_clean(self):
        email = self.cleaned_data['email'].lower().strip()
        new = InternalUser.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist.")
        return email

    class Meta:
        model = InternalUser
        fields = ['email', 'user_first_name',
                  'user_last_name', ]  # 'username',
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'text', 'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
            'password1': forms.PasswordInput(attrs={'type': 'text', 'class': 'form-control', }),
            'password2': forms.PasswordInput(attrs={'type': 'text', 'class': 'form-control', }),
        }
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Repeat Password',
        }


class InternalUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = InternalUser
        fields = ('email', 'user_first_name', 'user_last_name', 'password',
                  'user_start_date', 'user_discharge_date', 'user_auth_group',
                  'user_is_active', 'is_superuser', 'user_is_admin', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# class FireBaseAuthUserCreation(forms.Form):
#     verification_provider_type = forms.ChoiceField()

# the default login requires a username and a password
class InternalUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Enter the same email address as in your employee contact information',
        }),
        label='Email',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password.'
        }),
        label='Password',
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))

    class Meta:
        model = InternalUser


class InternalUserPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = InternalUser

# 2023-05-30
# this form is used to display a internal_user's employment information
# this detail page displays most but not all information of the talent record that is assocaited with the user.
# the fields shall be limited and not editable.


class EmploymentInfoForm(forms.ModelForm):
    # create a talent_full_name to store data from the property field of TalentsModel
    talent_full_name = forms.CharField(label="Full Name", required=False)

    class Meta:
        model = TalentsModel
        fields = ['talent_employee_id', 'talent_first_name', 'talent_last_name', 'talent_middle_name',
                  'talent_date_of_birth', 'talent_phone_number_primary', 'talent_mailing_address_is_the_same_physical_address',
                  'talent_hire_date', 'talent_department', 'talent_supervisor',
                  'talent_pay_type', 'talent_pay_rate', 'talent_pay_frequency',
                  'talent_previous_department',
                  ]

    def set_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

    def get_pay_type_display(self):
        return dict(self.PAY_TYPES).get(self.talent_pay_type)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_readonly()
        if self.instance:
            self.fields['talent_full_name'].initial = self.instance.talent_full_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('talent_employee_d', css_class='form-control'),
                Field('talent_first_name', css_class='form-control'),
                css_class='card'
            ),
            Div(
                Field('talent_department'),
                Field('talent_supervisor'),
                Field('talent_pay_type'),
                Field('talent_pay_rate'),
                Field('talent_pay_frequency'),
                css_class='card'
            ),
            Div(
                Field('talent_previous_department'),
                Field('talent_discharge_date'),
                css_class='card'
            ),
            # Add more sections for other groups of fields
        )

# a new admin authentication form
# 2023-06-06


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    # username = None
    email = forms.EmailField(label='Admin Email', max_length=254)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password.'
        }),
        label='Password',
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = InternalUser
        # fields = ('email', 'password',)
