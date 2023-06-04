from django import forms
from talent_management.models import TalentsModel, TalentDocuments
from datetime import date
from django.db.models import Q
# version 1 - talent creation form
class TalentsCreationForm(forms.ModelForm):
    
    def clean_email(self):
        talent_email = self.cleaned_data.get('talent_email').lower()
        
        talent = TalentsModel.objects.filter(talent_is_active=True).get(talent_email=talent_email)
        if not talent:
            return talent_email
        else:
            raise ValueError('this email has been associated with an exisitng active employee')

    class Meta:
        model = TalentsModel
        fields = ('talent_first_name', 'talent_last_name', 'talent_last_name', 
                   'talent_email', 'talent_phone_number_primary', 'talent_date_of_birth',
                   'talent_physical_address_01','talent_mailing_address_02',
                   'talent_physical_address_city','talent_physical_address_state', 'talent_physical_address_zip_code',
                 )


# version 2- creation form. using wizardview
class PersonalContactInfoForm(forms.ModelForm):
    def clean_talent_email(self):
        talent_email = self.cleaned_data['talent_email']

        if TalentsModel.objects.filter(Q(talent_email=talent_email) | Q(talent_is_active=True)).exists():
            error_message = "This email is already in use. The talent record might already exist."
            error_attrs = {'class': 'alert alert-warning','role':"alert"}
            raise forms.ValidationError(error_message, params=error_attrs)

        return talent_email
    
    # check date of birth to ensure the new person is 17 years or older.
    def clean_talent_date_of_birth(self):
        talent_date_of_birth = self.cleaned_data['talent_date_of_birth']
        today = date.today()
        age = today.year - talent_date_of_birth.year

        if age < 17:
            raise forms.ValidationError("The age must be larger than 17 years old.")

        return talent_date_of_birth
    class Meta:
        model = TalentsModel
        fields = ['talent_first_name', 'talent_last_name', 'talent_middle_name', 'talent_preferred_name',
                  'talent_email','talent_phone_number_primary','talent_date_of_birth','talent_emergency_contact',
                  'talent_physical_address_01','talent_physical_address_02',
                   'talent_physical_address_city','talent_physical_address_state', 'talent_physical_address_zip_code',
                   'talent_mailing_address_country',
                   'talent_mailing_address_is_the_same_physical_address',
                   'talent_education_level','talent_certifications',
                   ]  # Replace with the actual fields you want to display in the Personal Info section
        widgets = {
                    'talent_first_name': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_last_name': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_middle_name': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_preferred_name': forms.TextInput(attrs={'class': 'form-control',}),

                    'talent_date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 
                                                                                        'placeholder': 'Select a date',
                                                                                        'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                                                                                        }),
                    'talent_email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your email',}),
                    'talent_phone_number_primary': forms.TextInput(attrs={'class': 'form-control','data-inputmask': "'mask': '+1(999)999-9999'"}),
                    'talent_physical_address_01': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter the street address of your primary address. No PO Box.'}),
                    'talent_physical_address_02': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_physical_address_city': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_physical_address_state': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_physical_address_zip_code': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_mailing_address_country': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_emergency_contact': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_education_level': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_certifications': forms.TextInput(attrs={'class': 'form-control',}),
                    'talent_mailing_address_is_the_same_physical_address':forms.CheckboxInput(attrs={'class':'form-check-input',
                                                                                                     'readonly':'readyonly'}),
        }
        # labels = {
        #     'talent_first_name':'Legal First Name (as in driver ID or passport)',
        #     'talent_last_name': 'Legal Last Name (as in driver ID or passport)',
        #     'talent_mailing_address_is_the_same_physical_address': 'Mailing address is the same as the physical address?',
        #     'talent_education_level':'Highest degree obtained',
        #     'talent_certifications':'accreditions and certifcations',

        # }

class EmploymentInfoForm(forms.ModelForm):
    class Meta:
        model = TalentsModel
        fields = ['talent_hire_date','talent_department','talent_supervisor',
                  'talent_pay_type', 'talent_pay_rate', 'talent_pay_frequency',
                  # 'talent_previous_department',
                  #'talent_discharge_date','talent_years_of_work',
                  ]  # Replace with the actual fields you want to display in the Employment Info section
        widgets={'talent_hire_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 
                                                                                        'placeholder': 'Select a date',
                                                                                        'type': 'date', 
                                                                                        }),
                'talent_department':forms.Select(attrs={'class': 'custom-select'}),
                 'talent_pay_rate': forms.NumberInput(attrs={'type': 'text','class': 'form-control',}),

        }


class RemarkAndCommentsForm(forms.ModelForm):
    class Meta:
        model = TalentsModel
        fields = ['talent_HR_remarks_json', 'talent_incident_record_json',]  # Replace with the actual fields you want to display in the Contact Info section


TALENT_CREATE_FORMS = [
    ('personal_and_contact_info', PersonalContactInfoForm),
    ('employment_info', EmploymentInfoForm),
    ('remarks_and_comments', RemarkAndCommentsForm),
]

class TalentDocumentsForm(forms.ModelForm):
    class Meta:
        model = TalentDocuments
        fields = ['talent_employment_docs']
