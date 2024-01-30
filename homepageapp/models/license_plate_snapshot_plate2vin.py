from .base import models, InternalUser


# model stores reponses of api calls to plate2vin by entering a combo of plate and state.
# use the combo of plate and state to determine if newer information need to be pulled.
class LicensePlateSnapShotsPlate2Vin(models.Model):
    id = models.BigAutoField(primary_key=True)
    api_url = models.URLField(max_length=500, null=True, blank=True)
    api_response = models.JSONField(null=True, verbose_name="api_response")
    license_plate = models.CharField(
        max_length=10, null=True, db_index=True)
    state = models.CharField(max_length=2, null=True, db_index=True)
    vin = models.CharField(max_length=17, db_index=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    make = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    trim = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=50, null=True)
    style = models.CharField(max_length=50, null=True)
    transmission = models.CharField(max_length=50, null=True)
    drive_type = models.CharField(max_length=20, null=True, blank=True)
    fuel = models.CharField(max_length=20, null=True, blank=True)
    color_name = models.CharField(max_length=50, null=True, blank=True)
    color_abbreviation = models.CharField(max_length=15, null=True, blank=True)
    # keeps 5 versions of any license plates
    version = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL,
                                   null=True, related_name='license_plate_searches')
    # added to fresh anytime a new api is called for the same license plate and state
    last_checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return ''.join(self.license_plate, '_', self.state)
        return '{}_{}'.format(self.license_plate, self.state)
        # return f'{self.license_plate}_{self.state}'
    class Meta:
        db_table = 'licenseplate_snapshots_plate2vin'
        ordering = ["-id", '-created_at', "license_plate", '-version']
        indexes = [
            models.Index(fields=['-created_at', 'license_plate', 'state']),
        ]


