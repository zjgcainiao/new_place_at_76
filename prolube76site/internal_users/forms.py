# 2023-04-01 chatGPT generated form ---

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import InternalUser
from django.contrib.auth.forms import UserCreationForm

class InternalUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

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

class InternalUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = InternalUser
        fields = ('email', 'password', 'user_first_name', 'user_last_name',  'user_permission_level', \
                  'user_pay_type', 'user_hired_date', 'user_discharge_date', 'physical_address_01', \
                  'physical_address_02', 'physical_address_city', 'physical_address_state', 'physical_address_zip_code', \
                  'user_is_active', 'user_is_admin','is_superuser',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

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
        address = f"{cleaned_data['address_line_1']} {cleaned_data['address_line_2']}".strip()
        city = cleaned_data['city'].strip()
        state = cleaned_data['state'].strip()
        zip_code = cleaned_data['zip_code'].strip()
        country_code = cleaned_data['country_code'].strip()

        if not address or not city or not state or not zip_code:
            raise forms.ValidationError("All address fields are required.")

        return cleaned_data

# class FireBaseAuthUserCreation(forms.Form):
#     verification_provider_type = forms.ChoiceField()