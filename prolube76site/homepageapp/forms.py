from django import forms
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model , RepairOrdersNewSQL02Model

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = CustomersNewSQL02Model
        fields = ['customer_id', 'customer_first_name','customer_last_name', 'customer_does_allow_SMS',]

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehiclesNewSQL02Model
        fields = ['vehicle_id','vehicle_cust_id','VIN_number','vehicle_memo_01','vehicle_odometer_1']
        # exclude = ('created_at', 'updated_at',)

# Create your views here.
class RepairOrderModelForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL02Model
        fields = ['repair_order_id','repair_order_customer',
                  'repair_order_phase',
                  'repair_order_created_as_estimate','repair_order_snapshot_order_total_amount']