
from .base import forms, FormHelper

from django.forms import formset_factory
from django.forms import inlineformset_factory
from .address_update import AddressUpdateForm
from .customer_update import CustomerUpdateForm
from .reapair_order_update import RepairOrderUpdateForm
from .part_item_update import PartItemUpdateForm
from .labor_item_update import LaborItemUpdateForm
from .note_item_update import NoteItemUpdateForm
from .customer_email import CustomerEmailForm

from homepageapp.models import LineItemsNewSQL02Model, PartItemModel, LaborItemModel, NoteItemsNewSQL02Model, \
    EmailsNewSQL02Model, CustomersNewSQL02Model, VehiclesNewSQL02Model, CustomerEmailsNewSQL02Model, \
    CustomerPhonesNewSQL02Model
    

RepairOrderFormSet = formset_factory(RepairOrderUpdateForm, extra=0)
CustomerFormSet = formset_factory(CustomerUpdateForm, extra=0)
AddressFormset = formset_factory(AddressUpdateForm, extra=0)

EmailFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerEmailsNewSQL02Model, form=CustomerEmailForm, fields=('email',), extra=1)

PhoneFormset = inlineformset_factory(
    CustomersNewSQL02Model, CustomerPhonesNewSQL02Model, fields=('customer', 'phone'), fk_name='customer')

PartItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, PartItemModel,
                                              form=PartItemUpdateForm, extra=0,
                                              can_delete=True,
                                              )
LaborItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, LaborItemModel,
                                               form=LaborItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )


NoteItemInlineFormSet = inlineformset_factory(LineItemsNewSQL02Model, NoteItemsNewSQL02Model,
                                               form=NoteItemUpdateForm,
                                               extra=0,
                                               can_delete=True,
                                               )
# LineItem  UpdateForm. Parent formto PartItemUpdateForm and LaborItemUpdateForm.


LiteCustomerVehicleUpdateFormset = inlineformset_factory(
    CustomersNewSQL02Model, VehiclesNewSQL02Model, edit_only=True,
    fields=('vehicle_id', 'VIN_number', 'vehicle_license_plate_nbr'), fk_name='vehicle_cust')


