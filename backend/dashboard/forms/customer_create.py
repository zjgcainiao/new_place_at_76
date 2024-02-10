from .base import forms
from .customer_update import CustomerUpdateForm


class CustomerCreateForm(CustomerUpdateForm):
    class Meta(CustomerUpdateForm.Meta):
        fields = CustomerUpdateForm.Meta.fields  # + ['any_additional_field']

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # child form specific code
