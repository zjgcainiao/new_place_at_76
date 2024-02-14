from .customer_update import CustomerUpdateForm
from .base import formset_factory

CustomerFormset = formset_factory(CustomerUpdateForm, extra=0)