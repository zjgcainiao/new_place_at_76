from .base import forms
import phonenumbers
class CustomerUserRegisterFirebase(forms.Form):
    """
    A form for registering a new user with Firebase.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    display_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=30, required=False)

    class Meta:
        fields = ['email', 'password', 'display_name', 'phone_number']

    def clean_phone_number(self):
        # Add your code here
        
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phonenumbers.is_valid_number(phone_number):
            raise forms.ValidationError("Invalid phone number")
        return phone_number