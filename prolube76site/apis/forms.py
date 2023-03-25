from django import forms
from apis.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = CustomersNewSQL01Model
        fields = ['ustomer_id','customer_first_name','customer_last_name','customer_does_allow_SMS','customer_last_updated_datetime']

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehiclesNewSQL01Model
        fields =['vehicle_id','vehicle_cust_id','VIN_number','vehicle_memo_01','vehicle_odometer_1']

# Create your views here.
class RepairOrderModelForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL01Model
        fields=['repair_order_id','repair_order_created_as_estimate','repair_order_snapshot_order_total_amount']