from .base import forms, TalentsModel,Q
from .talent_create import TalentCreateForm


class TalentUpdateForm(TalentCreateForm):
    class Meta(TalentCreateForm.Meta):
        fields = TalentCreateForm.Meta.fields  # + ['any_additional_field']

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # override the method so excluding the current self.instance.id and see if there is any match. if so, then its troublesome.
    # the email should not exist in any other active talent record other than this Talent Id.
    def clean_talent_email(self):
        talent_email = self.cleaned_data['talent_email'].lower()

        if not talent_email:
            raise forms.ValidationError('email cannot be empty.')

        # If the instance has an ID, it means it's an update operation and not a creation
        if self.instance.pk:
            # Check if any active talent has this email but exclude the current instance from the queryset
            if TalentsModel.objects.filter(Q(talent_email=talent_email) & Q(talent_is_active=True)).exclude(pk=self.instance.pk).exists():
                error_message = "This email is already in use by another active talent."
                error_attrs = {'class': 'alert alert-warning', 'role': "alert"}
                raise forms.ValidationError(error_message, params=error_attrs)
        else:
            # If there's no instance ID, fall back to the original email validation logic
            return super().clean_talent_email()

        return talent_email