
from .base import forms, ValidationError
from core_operations.constants import LIST_OF_STATES_IN_US

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
