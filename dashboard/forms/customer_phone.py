from .base import forms

from homepageapp.models import PhonesNewSQL02Model, CustomerPhonesNewSQL02Model

PHONE_TYPES = [
    ('1', 'Home'),
    ('2', 'Work'),
    ('3', 'Mobile'),
    ('4', 'Fax'),
    ('5', 'Other'),
]
class CustomerPhoneForm(forms.ModelForm):
    customer = forms.CharField(label='customer_id')
    phone_desc_id = forms.ChoiceField(choices=PHONE_TYPES, label='type')

    phone_number = forms.CharField(
        max_length=20, label='phone number (10-digit)')
    phone_number_ext = forms.CharField(max_length=20, label='ext')

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # Save the related object (EmailsNewSQL02Model instance)
        phone = PhonesNewSQL02Model.objects.create(
            phone_desc_id=self.cleaned_data['phone_desc_id'],
            phone_number=self.cleaned_data['phone_number'],
            phone_number_ext=self.cleaned_data['phone_number_ext'],
        )
        instance.phone = phone

        if commit:
            instance.save()

        return instance

    class Meta:
        model = CustomerPhonesNewSQL02Model
        fields = ['customer', 'phone']
