from django import forms
import googlemaps
import  requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django.core.exceptions import ValidationError
from core_operations.validators import validate_us_state, validate_zip_code, 
from core_operations.constants import LIST_OF_STATES_IN_US

# address validting form
class AddressForm(forms.Form):
    address_line_1 = forms.CharField(max_length=100,required=True, label='Street Address, including Apt, Suite, Unit, etc.',
                                     required=True,
                                     placeholder='ex. 123 Main St. Apt 330')
    address_line_2 = forms.CharField(max_length=100, 
                                     required=False, 
                                     label='company name, c/o, etc.',
                                        placeholder='ex. c/o Jane Doe'
                                     )
    city = forms.CharField(max_length=50,required=True)
    state = forms.ChoiceField(choices=[('', '--- None ---')] + list(LIST_OF_STATES_IN_US), 
                              validators=[validate_us_state],
                              widget=forms.Select(attrs={'class': 'form-select'}))
    zip_code = forms.CharField(max_length=5,required=True,validators=[validate_zip_code])
    country_code = forms.CharField(max_length=10, required=False, initial='US', disabled=True)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'validate_address_manual'
            self.helper.form_id = 'validate-address-form'
            self.helper.form_tag = False
            self.helper.layout = Layout(
                Row(
                    Column(Field('address_line_1', css_class='form-control'), css_class=' col-md-8 mb-0'),
                    Column(Field('address_line_2', css_class='form-control'), css_class=' col-md-4 mb-0'),
                    css_class='form-group'
                ),
                Row(
                    Column(Field('city',css_class='form-control'), css_class='col-md-4 mb-0'),
                    Column(Field('state',css_class='form-control'), css_class='col-md-4 mb-0'),
                    Column(Field('zip_code',css_class='form-control'), css_class='col-md-4 mb-0'),
                    
                    css_class='form-row' # form-group, form-row
                ),
                Column(Field('country_code',css_class='border-0'),css_class='col-md-12 mb-0'),
            )
    def clean(self):
        cleaned_data = super().clean()
        address = f"{cleaned_data['address_line_1']} {cleaned_data['address_line_2']}".strip(
        )
        city = cleaned_data['city'].strip()
        state = cleaned_data['state'].strip()
        zip_code = cleaned_data['zip_code'].strip()
        country_code = cleaned_data['country_code'].strip()

        if not address or not city or not state or not zip_code:
            raise ValidationError("All address fields are required.")

        return cleaned_data
