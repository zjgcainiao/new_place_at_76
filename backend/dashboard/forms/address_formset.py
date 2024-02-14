from .base import formset_factory
from .address_update import AddressUpdateForm

AddressFormset = formset_factory(AddressUpdateForm, extra=0)