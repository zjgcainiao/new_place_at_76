from .base import forms
from core_operations.constants import EMAIL_TYPES
from homepageapp.models import AddressesNewSQL02Model

class CustomerAddressForm(forms.ModelForm):
    address_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    address_description = forms.CharField(max_length=20, label='description')
    address_company_or_ATTN = forms.CharField(
        max_length=20, label='Attention To or Company')
    address_line_01 = forms.CharField(
        max_length=20, label='Attention To or Company')
    address_city = forms.CharField(max_length=20, label='city')
    address_state = forms.CharField(max_length=2, label='state')
    address_zip_code = forms.CharField(max_length=10, label='zip code')

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # # Save the related object (EmailsNewSQL02Model instance)
        # address = AddressesNewSQL02Model.objects.create(
        #     id=self.cleaned_data['email_type_id'],
        #     email_address=self.cleaned_data['email_address']
        # )
        # instance.email = email

        if commit:
            instance.save()

        return instance
