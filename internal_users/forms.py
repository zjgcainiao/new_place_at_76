# 2023-04-01 chatGPT generated form ---

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import InternalUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from talent_management.models import TalentsModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox, ReCaptchaV3
from django.contrib.auth import authenticate
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, ButtonHolder, Submit, Row, Column, Button, Hidden
from crispy_forms.bootstrap import PrependedText, FormActions
class InternalUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)
    captcha =  ReCaptchaField(widget=ReCaptchaV2Invisible,
                              label='please check the box below to verify you are not a robot.')
    class Meta:
        model = InternalUser
        fields = ['id', 'email', 
                  'user_first_name', 'user_middle_name','user_last_name',
                  'password1', 'password2', 
                  ]
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        new = InternalUser.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist.")
        return email

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
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'internal_user_creation_form'
            # 'form-inline'  # 'form-horizontal'
            self.helper.form_class = 'form-horizontal'
            self.helper.form_tag = False
            self.helper.form_method = "post"
            # self.helper.form_action = reverse(
            #     'shops:search_by_vin_or_plate')  # Use your URL name here
            self.helper.layout = Layout(
                Row (
                    Column(Field('email',css_class='form-control'),css_class='col-md-12 mb-2'),
                css_class='form-group m-1'),
                Row (
                    Column(Field('user_first_name',css_class='form-control'),css_class='col-md-6 mb-2'),
                    Column(Field('user_middle_name',css_class='form-control'),css_class='col-md-6 mb-2'),
                    Column(Field('user_last_name',css_class='form-control'),css_class='col-md-6 mb-2'),
                css_class='form-group m-1'),

                Row (
                    Column(Field('password1',css_class='form-control'),css_class='col-md-6 mb-3'),
                    Column(Field('password2',css_class='form-control'),css_class='col-md-6 mb-3'),
                    css_class='form-group m-1'),    
                'captcha',
                ButtonHolder(
                    Submit('submit', 'Submit',css_class='btn btn-outline-primary'),
                ),
            )
# version 2 --- via UserCreationForm, AuthenticationForm
# 2023-04-26-chat-GPT-enabled


class InternalUserRegistrationFormV2(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        help_text='Required. Enter the very email address that is registed with the company.')
    user_first_name = forms.CharField(
        max_length=50, required=True, help_text='Required.')
    user_middle_name = forms.CharField(
        max_length=50, required=False, help_text='Optional.')
    user_last_name = forms.CharField(
        max_length=50, required=True, help_text='Required.')

    # this function will have to expand for employee email verifications.
    # employee record shall be created first before a user can be added.
    password1 = forms.CharField(label='Password', 
                                widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Enter Password'})
                                )
    password2 = forms.CharField(
        label='Repeat password', 
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Enter Password'})
        )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),
                             label='please check the box below to verify you are not a robot.')

    def clean_email(self):
            email = self.cleaned_data['email'].lower().strip()
            new = InternalUser.objects.filter(email=email)
            if new.count():
                raise ValidationError(" Email Already Exist.")
            return email

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

    class Meta:
        model = InternalUser
        fields = ['id', 'email', 
                  'user_first_name', 'user_middle_name','user_last_name',
                  'password1', 'password2', 
                  ]
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'text', 'class': 'form-control', }),
            'user_first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
            'user_middle_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
            'user_last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', }),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', }),
        }
        labels = {
            'email': 'Email',
            'user_first_name': 'First Name',
            'user_middle_name': 'Middle Name',
            'user_last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Repeat Password',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'internal_user_creation_form_v2'
        # 'form-inline'  # 'form-horizontal'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        # self.helper.form_action = reverse(
        #     'shops:search_by_vin_or_plate')  # Use your URL name here
        self.helper.layout = Layout(
            Row (
                Column(Field('email',css_class='form-control'),css_class='col-md-12'),
            css_class='form-group m-1'),
            Row (
                Column(Field('user_first_name',css_class='form-control'),css_class='col-md-6 mb-3'),
                Column(Field('user_middle_name',css_class='form-control'),css_class='col-md-6 mb-3'),
                Column(Field('user_last_name',css_class='form-control'),css_class='col-md-6 mb-3'),
            css_class='form-row '),

            Row (
                Column(Field('password1',css_class='form-control p-1 m-1'),css_class='col-md-6 mb-3'),
                Column(Field('password2',css_class='form-control p-1 m-1'),css_class='col-md-6 mb-3'),
                css_class='form-row'),
            
            Row('captcha',css_class='form-group'),

            Row (
                Button('submit', 'Submit',css_class='btn btn-outline-primary'),
            ),
        )

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
        model = InternalUser
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_tag = False
        # self.helper.form_method = "post"
        # self.helper.form_action = reverse(
        #     'shops:search_by_vin_or_plate')  # Use your URL name here
        # self.helper.layout = Layout(
        #     Div(
        #         Field('username', css_class='my-3'),
        #         HTML("""
        #             {% if form.username.errors %}
        #             <div class="alert alert-danger" role="alert">
        #                 {{ form.username.errors }}
        #             </div>
        #             {% endif %}
        #         """),
        #         css_class='form-label'
        #     ),
        #     Div(
        #         'password',
        #         HTML("""
        #             <div class="input-group-append">
        #                 <span class="input-group-text password-eye"></span>
        #             </div>
        #             <a href="{% url 'internal_users:password_reset' %}" class="fw-bold float-end">
        #                 <small>Forgot your password?</small>
        #             </a>
        #             {% if form.password.errors %}
        #             <div class="alert alert-danger" role="alert">
        #                 {{ form.password.errors }}
        #             </div>
        #             {% endif %}
        #         """),
        #         css_class='input-group my-3',
        #     ),
        #     Div(
        #         Field('remember_me', css_class='form-check-input', style="font-family: 'Orbitron',sans-serif;"),
        #         HTML("""
        #             <label class="form-check-label" for="checkbox-signin">Remember me</label>
        #         """),
        #         css_class='form-check'
        #     ),
        #     FormActions(
        #         Submit('submit', 'Log In', css_class='btn btn-outline-dark')
        #     )
        # )

class InternalUserPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = InternalUser

# added on 2023-08-23 to customize internal user password change forms.


class InternalUserPasswordChangeForm(PasswordChangeForm):
    email_or_phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    # Overriding the default fields
    def __init__(self, user, *args, **kwargs):
        super(InternalUserPasswordChangeForm,
              self).__init__(user, *args, **kwargs)
        # rename the original 'old_password' field to not confuse
        self.fields['old_password'].label = "Old password"
        # remove the username field from the original form
        # del self.fields['username']

    # Overriding the clean method to add our custom validation
    def clean(self):
        cleaned_data = super().clean()

        email_or_phone = cleaned_data.get('email_or_phone')
        old_password = cleaned_data.get('old_password')

        if email_or_phone and old_password:
            # Try to authenticate using email
            user = authenticate(email=email_or_phone, password=old_password)

            if user is None:
                # If authentication fails, try to authenticate using phone
                user = authenticate(
                    phone_number=email_or_phone, password=old_password)

            # If authentication still fails, raise an error
            if user is None:
                raise ValidationError("Invalid login details provided.")

        return cleaned_data

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
