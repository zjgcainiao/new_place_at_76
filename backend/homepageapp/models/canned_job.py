from .base import models, InternalUser
from .category import CategoryModel
# from .canned_job_line_item_sequence import CannedJobLineItemSequence

class CannedJobsNewSQL02Model(models.Model):
    canned_job_id = models.AutoField(primary_key=True)
    canned_job_title = models.CharField(max_length=50, null=True)
    canned_job_description = models.CharField(max_length=200, null=True)
    canned_job_is_in_quick_menu = models.BooleanField(default=False)
    canned_job_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True)

    canned_job_applied_year = models.CharField(max_length=10, blank=True, null=True)
    canned_job_applied_make_id = models.CharField(max_length=20,blank=True, null=True)
    canned_job_applied_submodel_id = models.CharField(max_length=20,blank=True, null=True)
    canned_job_vehicle_class = models.CharField(
        max_length=50, null=True, blank=True)
    
    # use string-based model reference to avoid circular import
    line_items = models.ManyToManyField('homepageapp.LineItemsNewSQL02Model', 
                                        through='homepageapp.CannedJobLineItemSequence', through_fields=('canned_job', 'line_item'))
    canned_job_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    canned_job_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='canned_job_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='canned_job_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'cannedjobs_new_03'
        ordering = ["-canned_job_id"]

    def __str__(self):
        return self.canned_job_title