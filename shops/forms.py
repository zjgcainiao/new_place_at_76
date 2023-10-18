from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime


class VINSearchForm(forms.Form):
    vin = forms.CharField(label='vin', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholer': 'enter full vin number.'}))
    year = forms.IntegerField(label='Model Year', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'enter model year'}))

    def clean_vin(self):
        vin = self.cleaned_data['vin']

        # Strip spaces
        vin = vin.replace(" ", "")

        # Check if it has 17 digits
        if len(vin) != 17:
            raise ValidationError(
                'VIN must have 17 non-empty digits')

        # Capitalize the VIN
        return vin.upper()

    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = datetime.now().year

        # Check if year is valid
        if year > current_year + 1 or year < 1900:  # Assuming no vehicle will be from before 1900
            raise forms.ValidationError(
                f'Model year must be between 1900 and {current_year + 1}')
        return year

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id


class LicensePlateSearchForm(forms.Form):
    license_plate = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter license plate number.'}))
    state = forms.ChoiceField(choices=[('', '--- None ---')] + list(LIST_OF_STATES_IN_US), widget=forms.Select(
        attrs={'class': 'form-select'}))

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        if len(license_plate) > 10:
            raise ValidationError(
                'License plate number must not be more than 10 characters long.')
        return license_plate.strip().upper()

    def clean_state(self):
        state = self.cleaned_data['state']
        if state and state not in dict(LIST_OF_STATES_IN_US):
            raise ValidationError('Invalid US state abbreviation.')
        return state

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # exclude the line item id
