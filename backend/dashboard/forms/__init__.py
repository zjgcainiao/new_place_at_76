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
# from .lite_customer_vehicle_update_formset import LiteCustomerVehicleUpdateFormset <--- could be redundant 
from .line_item_create import LineItemCreateForm
from .canned_job_update import CannedJobUpdateForm
from .canned_job_line_item_sequence_formset import CannedJobLineItemSequenceInlineFormset
from .phone_inline_formset import PhoneInlineFormset
from .customer_formset import CustomerFormset
from .address_formset import AddressFormset
from .email_inline_formset import EmailInlineFormset
from .lite_customer_vehicle_udpate_form import LiteCustomerVehicleUpdateInlineFormset
from .repair_order_formset import RepairOrderFormset
from .part_item_inline_formset import PartItemInlineFormset
from .labor_item_inline_formset import LaborItemInlineFormset
from .note_item_inline_formset import NoteItemInlineFormset




                        
                        