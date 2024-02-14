from .base import inlineformset_factory
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model

LiteCustomerVehicleUpdateInlineFormset = inlineformset_factory(
    CustomersNewSQL02Model, VehiclesNewSQL02Model, edit_only=True,
    fields=('vehicle_id', 'VIN_number', 'vehicle_license_plate_nbr'), fk_name='vehicle_cust')
