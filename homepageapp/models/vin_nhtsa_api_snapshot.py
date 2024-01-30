from .base import models, InternalUser
from .nhtsa_variable_list import NhtsaVariableList
from apis.api_vendor_urls import NHTSA_API_URL

# this model stores each snapshot pulled for each vin from NHTSA gov website.
class VinNhtsaApiSnapshots(models.Model):
    # Assuming standard VIN length of 17 characters. NHTSA website
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(
        max_length=17, verbose_name="Vehicle Identification Number (VIN)")
    variable = models.ForeignKey(
        NhtsaVariableList,
        on_delete=models.SET_NULL, null=True,
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

    class Meta:
        db_table = 'vin_snapshots_nhtsa_new_03'
        ordering = ['-id', '-created_at', 'vin', ]
        indexes = [
            # Index to speed up searches based on created at, VIN and VariableID
            models.Index(fields=['-created_at', 'vin', ]),
        ]

    def __str__(self):
        return f"{self.vin} - {self.variable_name}: {self.value}"
