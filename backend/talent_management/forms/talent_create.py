from .base import TalentsModel, forms, LIST_OF_STATES_IN_US, date, \
    FormHelper, Layout, Fieldset, Submit, Field, ButtonHolder, HTML, Reset, Column, Row, Div, Button, \
    gettext_lazy as _

class TalentCreateForm(forms.ModelForm):
    talent_first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Legal First Name (as in driver license (DL) or passport)')
    talent_last_name = forms.CharField(
        required=True, label='Legal Last Name (as in driver license(DL) or passport)')
    talent_middle_name = forms.CharField(required=False, label='Middle Name')
    talent_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email address will be used to create company user profile.', }), required=True, label='Email', help_text='email address should be unique to each talent record.')
    talent_physical_address_state = forms.ChoiceField(
        choices=LIST_OF_STATES_IN_US, required=False, label='State')

    class Meta:
        model = TalentsModel
        fields = ['talent_first_name', 'talent_last_name', 'talent_middle_name', 'talent_preferred_name',
                  'talent_email', 'talent_phone_number_primary', 'talent_date_of_birth',
                  'talent_emergency_contact',
                  'talent_physical_address_01', 'talent_physical_address_02',
                  'talent_physical_address_city', 'talent_physical_address_state', 'talent_physical_address_zip_code',
                  'talent_physical_address_country',
                  'talent_mailing_address_is_the_same_physical_address',
                  'talent_education_level', 'talent_certifications',
                  # payroll related fields
                  'talent_ssn', 'talent_hire_date', 'talent_department', 'talent_supervisor',
                  'talent_pay_type', 'talent_pay_rate', 'talent_pay_frequency',
                  # additional comment and document forms.
                  'talent_HR_remarks_json', 'talent_incident_record_json',

                  ]  # Replace with the actual fields you want to display in the Personal Info section
        widgets = {

            'talent_date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control',
                                                                                'placeholder': 'Select a date',
                                                                                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                                                }),
            'talent_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', }),
            'talent_phone_number_primary': forms.TextInput(attrs={'class': 'form-control', 'data-inputmask': "'mask': '+1(999)999-9999'"}),
            'talent_physical_address_01': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter the street address of your primary address. No PO Box.'}),
            'talent_physical_address_02': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_physical_address_city': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_physical_address_state': forms.Select(attrs={'class': 'form-select', }),
            'talent_physical_address_zip_code': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_mailing_address_country': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_emergency_contact': forms.TextInput(attrs={'placeholder': 'we highly recommend our employee to enter emergency contact. John Cooper 203-029-0930. ', }),
            'talent_education_level': forms.TextInput(attrs={}),
            'talent_certifications': forms.TextInput(attrs={'type': 'text'}),
            'talent_mailing_address_is_the_same_physical_address': forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                                              'readonly': 'readyonly'}),
            'talent_mailing_address_01': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter the mailing address if different from your street address'}),
            'talent_mailing_address_02': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_mailing_address_city': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_mailing_address_state': forms.Select(attrs={'class': 'form-select', }),
            'talent_maling_address_zip_code': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_mailing_address_country': forms.TextInput(attrs={'class': 'form-control', }),

            'talent_hire_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control',
                                                                            'placeholder': 'Select a date',
                                                                            'type': 'date',
                                                                            }),
            'talent_department': forms.Select(attrs={'class': 'custom-select'}),
            'talent_pay_type': forms.Select(attrs={'class': 'custom-select'}),
            'talent_pay_frequency': forms.Select(attrs={'class': 'form-select'}),
            'talent_pay_rate': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),

        }
        labels = {
            'talent_first_name': 'Legal First Name (as in driver ID or passport)',
            'talent_last_name': 'Legal Last Name (as in driver ID or passport)',
            'talent_middle_name': 'Middle Name',
            'talent_ssn': "Social Security Number (SSN) or any form of tax ID (TINs)",
            'talent_mailing_address_is_the_same_physical_address': 'Mailing address is the same as the physical address?',
            'talent_education_level': 'Highest degree obtained',
            'talent_certifications': 'Accreditions and Certifcations',
            'talent_physical_address_country': 'Country',
            'talent_emergency_contact': 'Emergency Contact',
            'talent_physical_address_city': 'City',
            'talent_physical_address_state': 'State',
            'talent_physical_zip_code': 'Zip Code',
            'talent_phone_number_primary': 'Primary Phone Number'

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        formatted_state_choices = [
            (abbr, f"{abbr} - {full}") for abbr, full in LIST_OF_STATES_IN_US]
        # license state can be only chosen from a list. Display custom data when there is no match.

        self.fields['talent_physical_address_state'].choices = formatted_state_choices

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = "post"
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-9'
        self.helper.layout = Layout(
            Fieldset(_('Personal'),
                     Row(Column(Field('talent_first_name', css_class='form-control'),
                                css_class='col-mb-3',),
                         Column(Field('talent_last_name', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-mb-3',),
                         Column(Field('talent_middle_name', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-mb-3',),
                         Column(Field('talent_email', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-mb-3',),
                         Column(Field('talent_phone_number_primary', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-mb-3',),
                         Column(Field('talent_date_of_birth', css_class='form-control'),  # style="background-color: #333"
                                css_class='col-mb-3',),
                         css_class=' mb-0'),
                     Row(HTML("<hr>"),
                         css_class='m-1 p-1'),
                     Row(Column(Field('talent_physical_address_01'),
                                css_class='col-mb-3',),
                         Column(Field('talent_physical_address_02'),
                                css_class='col-mb-3',),
                         Column(Field('talent_physical_address_city'),
                                css_class='col-mb-3',),
                         Column(Field('talent_physical_address_state'),
                                css_class='col-mb-2',),
                         Column(Field('talent_physical_address_zip_code'),
                                css_class='col-mb-2',),
                         Column(Field('talent_physical_address_country'),
                                css_class='col-mb-2',),
                         css_class=' mb-0'),
                     css_class='m-1'),
            Fieldset(_('HR Records'),
                     Row(Column(Field('talent_HR_remarks_json', css_class='form-control'),
                                css_class='col-mb-6',),
                         Column(Field('talent_incident_record_json', css_class='form-control'),
                                css_class='col-mb-6',),

                         css_class='pt-1 mb-0'),
                     css_class=' m-1'),

            ButtonHolder(
                Row(Column(Submit('submit', 'Submit', css_class='btn btn-primary',
                                  css_id='submit-button',),
                           css_class='col col-mb-3',),
                    Column(Button('cancel', 'Cancel', css_class='btn btn-secondary', ),
                           css_class='col col-mb-3',),

                    css_class='pt-1 mb-0'),



            ),

        )

    def clean_talent_email(self):
        talent_email = self.cleaned_data['talent_email'].lower()
        if not talent_email:
            raise forms.ValidationError('talents email cannot be empty.')
        else:
            if TalentsModel.objects.filter(Q(talent_email=talent_email) & Q(talent_is_active=True)).exists():
                error_message = "This email is already in use. The talent record might already exist."
                error_attrs = {'class': 'alert alert-warning', 'role': "alert"}
                raise forms.ValidationError(error_message, params=error_attrs)

            return talent_email

    def clean_name_field(self, field_name, error_msg):
        name = self.cleaned_data.get(field_name, '').strip()
        name = name.lower().capitalize() if name else None

        if not name:
            raise forms.ValidationError(error_msg)
        return name

    def clean_talent_first_name(self):
        return self.clean_name_field('talent_first_name', "Talent's first name can not be empty.")

    def clean_talent_last_name(self):
        return self.clean_name_field('talent_last_name', "Talent's last name can not be empty.")

    # check date of birth to ensure the new person is 17 years or older.

    def clean_talent_date_of_birth(self):
        talent_date_of_birth = self.cleaned_data['talent_date_of_birth']
        today = date.today()
        age = today.year - talent_date_of_birth.year

        if age < 17:
            raise forms.ValidationError(
                "The age must be larger than 17 years old.")

        return talent_date_of_birth
