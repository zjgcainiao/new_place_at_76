
from .base import models

# a comprehensive model for vin that combine all other vin related models: nftsa saftey reating, recalls, manufacture information of the vehicle,
# via the internal lookup across RepairOrder, this model can also provides the repair history of the vehicle when aviailable. 
# the model can also be used to store the vehicle's registration information, and insurance information.
# Vin Model stores the most comprehensive information about a vehicle,
# it collect information from multiple sources, including NHTSA, RepairOrder, and other sources. Each source has its own model. 
# by defining multiple foreign keys to these source models, this model can be used to store the comprehensive information about a vehicle.

class Vin(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=30, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vin'
        ordering = ["-id", 'vin']

    def __str__(self):
        return self.vin