from .vehicle_update import VehicleUpdateForm

class VehicleCreateForm(VehicleUpdateForm):
    class Meta(VehicleUpdateForm.Meta):
        fields = VehicleUpdateForm.Meta.fields  # + ['any_additional_field']

    # Add any additional fields or methods specific to the create form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # child form specific code