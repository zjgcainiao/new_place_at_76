from .base import forms, inlineformset_factory
from .customer_email import CustomerEmailForm
from homepageapp.models import CustomersNewSQL02Model, CustomerEmailsNewSQL02Model

EmailInlineFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerEmailsNewSQL02Model, form=CustomerEmailForm, fields=('email',), extra=1)