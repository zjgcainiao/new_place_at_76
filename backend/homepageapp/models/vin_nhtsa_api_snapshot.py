from .base import models, InternalUser
from .nhtsa_variable_list import NhtsaVariableList
from apis.api_vendor_urls import NHTSA_API_URL
from shops.models import Vin
# this model stores each snapshot pulled for each vin from NHTSA gov website.
class VinNhtsaApiSnapshots(models.Model):
    # Assuming standard VIN length of 17 characters. NHTSA website
    id = models.BigAutoField(primary_key=True)

    vin = models.ForeignKey(
        Vin,
        on_delete=models.DO_NOTHING, 
        related_name='nhtsa_snapshots',
        to_field='vin',  # Ensure this matches the unique identifier in the Vin model.
                )
    variable = models.ForeignKey(
        NhtsaVariableList,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        to_field='variable_id',  # specify the field of the related model is variable_id
        related_name='nhtsa_variable_ids')
    variable_name = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    value_id = models.IntegerField(null=True, blank=True)
    source = models.CharField(
        max_length=300, default=NHTSA_API_URL, null=True, blank=True)
    results_count = models.IntegerField(null=True, blank=True)
    results_message = models.CharField(max_length=800, null=True, blank=True)
    results_search_criteria = models.CharField(
        max_length=300, null=True, blank=True)
    # keeps 5 versions of vin info pulled from nhtsa.gov
    version = models.IntegerField(default=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, 
        on_delete=models.DO_NOTHING, 
        null=True, blank=True,
        related_name='vin_nhtsa_snapshots_created_by')
    updated_by = models.ForeignKey(
        InternalUser, 
        on_delete=models.DO_NOTHING, 
        null=True, blank=True,
        related_name='vin_nhtsa_snapshots_updated_by')
    

    class Meta:
        db_table = 'vin_snapshots_nhtsa_new_03'
        ordering = ['vin','variable','-created_at',]
        indexes = [
            # Index to speed up searches based on created at, VIN and VariableID
            models.Index(fields=['vin','variable','-created_at', ]),
        ]

    def __str__(self):
        return f"{self.vin} - {self.variable_name}: {self.value}"
