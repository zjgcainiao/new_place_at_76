# dashboard/forms/__init__.py

from .automan_base import AutomanBaseForm
from .automan_base_model import AutomanBaseModelForm
from .search import SearchForm
from .customer_email import CustomerEmailForm
from .customer_address import CustomerAddressForm
from .customer_phone import CustomerPhoneForm
from .customer_update import CustomerUpdateForm
from .customer_create import CustomerCreateForm
from .reapair_order_update import RepairOrderUpdateForm
from .address_update import AddressUpdateForm
from .lite_email_update import LiteEmailUpdateForm
from .vehicle_create import VehicleCreateForm
from .vehicle_update import VehicleUpdateForm
from .part_item_update import PartItemUpdateForm
from .labor_item_update import LaborItemUpdateForm
from .note_item_update import NoteItemUpdateForm
from .line_item_update import LineItemUpdateForm
from .line_item_create import LineItemCreateForm
from .lite_email_update import LiteEmailUpdateForm
from .vin_search import VINSearchForm
from .license_plate_search import LicensePlateSearchForm
from .formsets import RepairOrderFormSet,CustomerFormSet,PartItemInlineFormSet, \
                        LaborItemInlineFormSet,NoteItemInlineFormSet,LiteCustomerVehicleUpdateFormset, \
                        AddressFormset, EmailFormset, PhoneFormset
# from .lite_customer_vehicle_update_formset import LiteCustomerVehicleUpdateFormset <--- could be redundant 
from .line_item_create import LineItemCreateForm