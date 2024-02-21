from .base import CustomerUser, AuthenticationForm,forms, FormHelper, Layout, Field, HTML

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
        help_text="stay logged in.",
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = CustomerUser
        # fields = ['cust_user_email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # ... other fields ...
            Field('password', template='password_field_with_toggle.html'),
            # ... other fields ...
        )
