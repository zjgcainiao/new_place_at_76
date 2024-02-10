from .base import forms, AuthenticationForm, InternalUser, \
    FormHelper, Layout, Div, Field, HTML, ButtonHolder, Submit, Row, Column, Button, Hidden
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
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.form_method = "post"
        # self.helper.form_action = reverse(
        #     'internal_users:internal_user_login')  # Use your URL name here
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