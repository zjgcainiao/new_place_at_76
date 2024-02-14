from .base import inlineformset_factory
from homepageapp.models import CustomersNewSQL02Model, CustomerPhonesNewSQL02Model


PhoneInlineFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerPhonesNewSQL02Model, fields=('customer', 'phone'), fk_name='customer')