from .base import forms
from .automan_base_model import AutomanBaseModelForm
from core_operations.constants import EMAIL_TYPES
from homepageapp.models import CustomerEmailsNewSQL02Model, EmailsNewSQL02Model


class CustomerEmailForm(AutomanBaseModelForm):
    email_type_id = forms.ChoiceField(choices=EMAIL_TYPES, label='type')
    email_address = forms.EmailField()

    class Meta:
        model = CustomerEmailsNewSQL02Model
        fields = ('email_type_id',)

    def save(self, commit=True):
        # Save the primary object (CustomerEmailsNewSQL02Model instance)
        instance = super().save(commit=False)

        # Save the related object (EmailsNewSQL02Model instance)
        email = EmailsNewSQL02Model.objects.create(
            email_type_id=self.cleaned_data['email_type_id'],
            email_address=self.cleaned_data['email_address']
        )
        instance.email = email

        if commit:
            instance.save()

        return instance
