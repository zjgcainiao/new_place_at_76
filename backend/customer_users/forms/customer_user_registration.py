from .base import forms, CustomerUser, UserCreationForm, AuthenticationForm, \
    ValidationError, validate_us_state, validate_zip_code, LIST_OF_STATES_IN_US, is_valid_us_phone_number, \
    re, RegexValidator, ReCaptchaField, ReCaptchaV2Checkbox, FormHelper, Layout, Row, Column, Field, ButtonHolder, Submit, HTML


class CustomerUserRegistrationForm(UserCreationForm):
    cust_user_email = forms.EmailField(help_text='Required. We will send important account updates and notifications to this email.',
                                       widget=forms.EmailInput(
                                           attrs={'type': 'email', 'class': 'form-control', }),
                                       label='Email',
                                       required=True)
    cust_user_phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                               'placeholder:': 'ex. 213-445-9990 or 2134459990. US phone number only.'}),
        help_text='Optional but recommended. We will text important updates to this phone number.', label='Phone Number')
    cust_user_last_name = forms.CharField(
        max_length=30, required=False, help_text='Your Last Name or Family Name. Optional.', label='Last Name', widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }))

    cust_user_middle_name = forms.CharField(
        max_length=30, required=False, help_text='Your Middle Name. Optional.', label='Middle Name')
    cust_user_first_name = forms.CharField(
        max_length=30, required=False,
        help_text='Your First Name. Optional.', label='First Name',
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                               'placeholder:': 'ex. John, Kelly, or if it is a business ABC Company or ABC Inc.'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),
                             label='please check the box below to verify you are not a robot.')
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
    #     api_params={'hl': 'en','onload': 'onloadCallback'}
    # ), label = 'please check the box below to verify you are not a robot.')

    class Meta:
        model = CustomerUser
        fields = ['cust_user_email', 'cust_user_phone_number',
                  'cust_user_first_name', 'cust_user_middle_name', 'cust_user_last_name',
                  'password1', 'password2']  # 'username',
        # required = ['cust_user_phone_number', 'cust_user_first_name', 'password1', 'password2']
        labels = {
            'password1': 'Password',
            'password2': 'Repeat Password',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # True
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column(Field('cust_user_email', css_class='form-control'),
                       css_class=' col-md-6 mb-0'),
                Column(Field('cust_user_phone_number',
                       css_class='form-control'), css_class=' col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('password1', css_class='form-control'),
                       css_class='col-md-6 mb-0'),
                Column(Field('password2', css_class='form-control'),
                       css_class='col-md-6 mb-0'),
                css_class='form-row'  # form-group, form-row
            ),
            Row(
                Column(Field('cust_user_first_name',
                       css_class='form-control'), css_class='col-md-4 mb-0'),
                Column(Field('cust_user_middle_name',
                       css_class='form-control'), css_class='col-md-4 mb-0'),
                Column(Field('cust_user_last_name',
                       css_class='form-control'), css_class='col-md-4 mb-0'),

                css_class='form-row'  # form-group, form-row
            ),
            Field('captcha', css_class=''),
            HTML("<hr>"),
            ButtonHolder(
                Submit('submit', 'Register',
                       css_class='automan-btn-primary justify-content-center'),

                # Column(Reset('Reset This Form', 'Reset Form', css_class='btn-outline-dark'),
                #         css_class='col col-6'),

                css_class='row justify-content-center'),
        )

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

        # if phone number is empty. skip validation
        if not phone_number:
            return None

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
            new = CustomerUser.objects.filter(email=email)
            if new.count():
                raise ValidationError(" Email Already Exists.")
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
