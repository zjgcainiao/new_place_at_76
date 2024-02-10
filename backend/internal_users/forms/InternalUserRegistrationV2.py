
from .base import forms, ReCaptchaField, ReCaptchaV2Checkbox, \
    InternalUser, ValidationError, re, FormHelper, Layout,Field, Row, Column, ButtonHolder, Button, Submit

class InternalUserRegistrationFormV2(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        help_text='Required. Enter the personal email address that is registered with the company.')
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
                raise ValidationError("Email Already Exist.")
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
        # widgets = {
        #     'email': forms.EmailInput(attrs={'type': 'text', 'class': 'form-control', }),
        #     'user_first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        #     'user_middle_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        #     'user_last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', }),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control', }),
        # }
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
            css_class='form-group'),

            Row (
                Column(Field('password1',css_class='form-control p-1 m-1'),css_class='col-md-6 mb-3'),
                Column(Field('password2',css_class='form-control p-1 m-1'),css_class='col-md-6 mb-3'),
                css_class='form-row'),
            
            Row('captcha',css_class='form-group'),

            ButtonHolder (
                Button('submit', 'Submit',css_class='btn btn-outline-primary'),
            ),
        )
