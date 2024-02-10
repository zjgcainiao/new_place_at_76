
from .base import forms, ReadOnlyPasswordHashField, InternalUser


class InternalUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = InternalUser
        fields = ('email', 'user_first_name', 'user_last_name', 'password',
                  'user_start_date', 'user_discharge_date', 'user_auth_group',
                  'user_is_active', 'is_superuser', 'user_is_admin', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

