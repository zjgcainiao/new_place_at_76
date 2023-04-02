from django import forms
from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model , RepairOrdersNewSQL01Model

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = CustomersNewSQL01Model
        fields = ['customer_id', 'customer_first_name','customer_last_name', 'customer_does_allow_SMS',]

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehiclesNewSQL01Model
        fields = ['vehicle_id','vehicle_cust_id','VIN_number','vehicle_memo_01','vehicle_odometer_1']
        # exclude = ('created_at', 'updated_at',)

# Create your views here.
class RepairOrderModelForm(forms.ModelForm):
    class Meta:
        model = RepairOrdersNewSQL01Model
        fields = ['repair_order_id','repair_order_created_as_estimate','repair_order_snapshot_order_total_amount']