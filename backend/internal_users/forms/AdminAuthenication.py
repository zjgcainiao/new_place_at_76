# a new admin authentication form
# 2023-06-06
from .base import AuthenticationForm, forms, InternalUser

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

