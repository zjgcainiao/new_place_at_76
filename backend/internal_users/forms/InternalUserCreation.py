from .base import forms, ReCaptchaField, ReCaptchaV2Checkbox, \
    InternalUser, ValidationError, re, FormHelper, Layout,Field, Row, Column, ButtonHolder, Submit

class InternalUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    user_full_name = forms.CharField(label='Full Name', 
                        required=True,
                        max_length=255,
                        help_text='Required. John R. Doe or John Doe.',
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    
    password1 = forms.CharField(label='Password', 
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),
                             label='please check the box below to verify you are not a robot.')
    # captcha =  ReCaptchaField(widget=ReCaptchaV2Invisible,
    #                           label='please check the box below to verify you are not a robot.')
    class Meta:
        model = InternalUser
        fields = ['id', 'email', 
                  'user_full_name',
                  'password1', 'password2', 
                  ]
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        new = InternalUser.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist.")
        return email
    
    def clean_user_full_name(self):
        full_name = self.cleaned_data['user_full_name'].strip()
        # Check if the name is empty
        if not full_name:
            raise ValidationError("Full name is required.")
        
        # Check for not-allowed characters (adjust the regex as needed)
        if re.search(r'[^a-zA-Z\s]', full_name):
            raise ValidationError("Full name contains invalid characters.")
        
        return full_name

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
        full_name = self.cleaned_data['user_full_name']
        name_parts = full_name.split()

        user.user_first_name = name_parts[0]
        user.user_middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else ''
        user.user_last_name = name_parts[-1] if len(name_parts) > 1 else ''

        
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
            #     'internal_users:internal_user_register')  # Use your URL name here
            self.helper.layout = Layout(
                Row (
                    Column(Field('email',wrapper_class=' px-1 mt-1'),css_class='col-md-6'),
                    Column(Field('user_full_name',wrapper_class='px-1 mt-1'),css_class='col-md-6'),
                css_class='form-group'),


                Row (
                    Column(Field('password1',wrapper_class='px-1 mt-1'),css_class='col-md-6 '),
                    Column(Field('password2',wrapper_class='px-1 mt-1'),css_class='col-md-6 '),
                    css_class='form-group'),    
                Row('captcha',css_class='form-group mt-1'),
                Row(ButtonHolder(
                    Submit('submit', 'Submit',css_class='btn btn-primary'),
                ),css='m-1'),
            )