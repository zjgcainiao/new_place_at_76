from .base import serializers
from homepageapp.models import VinNhtsaApiSnapshots, LicensePlateSnapShotsPlate2Vin

class LastestVinDataSerializer(serializers.ModelSerializer):

    # use to create a nested relationship
    flattened_data = serializers.SerializerMethodField()

    class Meta:
        model = VinNhtsaApiSnapshots
        fields = ['id', 'vin', 'flattened_data', 'variable', 'variable_name', 'value']
        depth = 1

    def get_flattened_data(self, obj):
        # Initialize an empty dictionary to store our flattened data
        flattened_data = {}

        # Access the related NhtsaVariableList object through the foreign key
        variable = obj.variable

        # Check if the variable exists and is not None
        if variable:
            # Use the attributes of the variable object as keys
            # and the corresponding value from VinNhtsaApiSnapshots as the value
            flattened_data[f"{variable.variable_name} (id:{variable.variable_id})"] = obj.value

        # Return the flattened data
        return flattened_data
