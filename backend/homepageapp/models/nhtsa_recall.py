from .base import models, InternalUser

class NhtsaRecall(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=30, null=True, blank=True)
    model_year = models.IntegerField(null=True,
                                     blank=True, db_index=True)
    make = models.CharField(max_length=100, null=True,
                            blank=True, db_index=True)
    model = models.CharField(max_length=50, null=True, db_index=True)

    manufacturer = models.CharField(
        max_length=100, null=True, blank=True)
    nhtsa_compaign_number = models.CharField(
        max_length=50, blank=True, null=True)
    park_it = models.BooleanField(
        null=True, blank=True)
    park_outside = models.BooleanField(
        null=True, blank=True)
    nhtsa_action_number = models.CharField(
        max_length=50, null=True, blank=True)
    
    report_received_date = models.DateField(
        null=True, blank=True, db_index=True)
    recall_component = models.CharField(
        max_length=4000, null=True, blank=True)
    recall_summary = models.CharField(max_length=4000, null=True, blank=True)
    recall_consequence = models.CharField(
        max_length=4000, null=True, blank=True)
    recall_remedy = models.CharField(max_length=4000, null=True, blank=True)

    recall_notes = models.CharField(max_length=4000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, related_name='recalls_created_by')
    # added to fresh anytime a new api is called for the same license plate and state
    last_checked_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, related_name='recalls_updated_by')

    def __str__(self):
        return '{}_{}_{}_{}_{}'.format(self.model_year,self.make,self.model, self.nhtsa_compaign_number, self.recall_summary)

    class Meta:
        db_table = 'nhtsa_recalls'
        ordering = ["-id", '-model_year', 'make',
                    'model', '-report_received_date']

        indexes = [
            models.Index(fields=['-model_year', 'make', 'model']),
        ]
