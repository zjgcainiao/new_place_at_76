from .base import forms, TalentsModel, LIST_OF_STATES_IN_US,date, Q


# version 2-creation form. using wizardview


class PersonalContactInfoForm(forms.ModelForm):
    talent_first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', }), label='Legal First Name (as in driver license (DL) or passport)')
    talent_last_name = forms.CharField(
        required=True, label='Legal Last Name (as in driver license(DL) or passport)')
    talent_middle_name = forms.CharField(required=False, label='Middle Name')
    talent_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email address will be used to create company user profile.', }), required=True, label='Email', help_text='email should be unique in each talent record.')
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
                  'talent_mailing_address_01', 'talent_mailing_address_02',
                  'talent_mailing_address_city', 'talent_mailing_address_state', 'talent_mailing_address_zip_code',
                  'talent_mailing_address_country',
                  'talent_education_level', 'talent_certifications',
                  ]  # Replace with the actual fields you want to display in the Personal Info section
        widgets = {

            'talent_date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control',
                                                                                'placeholder': 'Select a date',
                                                                                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                                                }),
            'talent_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', }),
            'talent_phone_number_primary': forms.TextInput(attrs={'data-inputmask': "'mask': '+1(999)999-9999'"}),
            'talent_physical_address_01': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter the street address of your primary address. No PO Box.'}),
            'talent_physical_address_02': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_physical_address_city': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_physical_address_state': forms.Select(attrs={'class': 'form-select', }),
            'talent_physical_address_zip_code': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_mailing_address_country': forms.TextInput(attrs={'class': 'form-control', }),
            'talent_emergency_contact': forms.TextInput(attrs={'placeholder': 'we highly recommend our employee to enter emergency contact. John Cooper 203-029-0930. ', }),
            'talent_education_level': forms.TextInput(attrs={}),
            'talent_certifications': forms.TextInput(attrs={'type': 'text'}),
            'talent_mailing_address_is_the_same_physical_address': forms.CheckboxInput(attrs={'class': 'form-check',
                                                                                              'style': "display:inline-block;margin-right:20px;"}),
        }
        labels = {
            'talent_mailing_address_is_the_same_physical_address': 'Mailing address is the same as the physical address?',
            'talent_education_level': 'Highest Degree obtained',
            'talent_certifications': 'Accreditions and Certifcations',
            'talent_physical_address_country': 'Country',
            'talent_emergency_contact': 'Emergency Contact',
            'talent_physical_address_city': 'City',
            'talent_physical_address_state': 'State',
            'talent_physical_address_zip_code': 'Zip Code',
            'talent_phone_number_primary': 'Primary Phone Number',

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # add a "form-control" class to each form input
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        formatted_state_choices = [
            (abbr, f"{abbr} - {full}") for abbr, full in LIST_OF_STATES_IN_US]
        # license state can be only chosen from a list. Display custom data when there is no match.

        self.fields['talent_physical_address_state'].choices = formatted_state_choices

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
