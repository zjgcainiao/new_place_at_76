
# added on 2023-08-23 to customize internal user password change forms.

from .base import forms, PasswordChangeForm, ValidationError, authenticate, reverse

class InternalUserPasswordChangeForm(PasswordChangeForm):
    email_or_phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    # Overriding the default fields
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # rename the original 'old_password' field to not confuse
        self.fields['old_password'].label = "Old password"
        # remove the username field from the original form
        # del self.fields['username']

    # Overriding the clean method to add our custom validation
    def clean(self):
        cleaned_data = super().clean()

        email_or_phone = cleaned_data.get('email_or_phone')
        old_password = cleaned_data.get('old_password')

        if email_or_phone and old_password:
            # Try to authenticate using email
            user = authenticate(email=email_or_phone, password=old_password)

            if user is None:
                # If authentication fails, try to authenticate using phone
                user = authenticate(
                    phone_number=email_or_phone, password=old_password)

            # If authentication still fails, raise an error
            if user is None:
                raise ValidationError("Invalid login details provided.")

        return cleaned_data
