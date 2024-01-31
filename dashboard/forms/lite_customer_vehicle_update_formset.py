from django.forms import inlineformset_factory
from dashboard.models import CustomersNewSQL02Model, VehiclesNewSQL02Model


LiteCustomerVehicleUpdateFormset = inlineformset_factory(
    CustomersNewSQL02Model, VehiclesNewSQL02Model, edit_only=True,
    can_delete=True,
    fields=('vehicle_id', 'VIN_number', 'vehicle_license_plate_nbr', 'vehicle_license_state'), 
    fk_name='vehicle_cust'),

