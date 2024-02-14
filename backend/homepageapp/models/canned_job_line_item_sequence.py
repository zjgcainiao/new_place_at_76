from .base import models, InternalUser
from .canned_job import CannedJobsNewSQL02Model
from .line_item import LineItemsNewSQL02Model
#   {
#     "CannedJobId": 161,
#     "LineItem": 498255,
#     "Sequence": 40,
#     "timestamp": "0x0000000002C9F5B1",
#     "CannedJobLineItemSequenceId": 216,
#     "RecordVersion": 1,
#     "LastChangeDate": "1900-01-01T00:00:00"
#   },
class CannedJobLineItemSequence(models.Model):
    id = models.BigAutoField(primary_key=True)
    canned_job = models.ForeignKey(
        CannedJobsNewSQL02Model, on_delete=models.DO_NOTHING, null=True, related_name='line_item_sequences')
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.DO_NOTHING, null=True, related_name='canned_job_of_line_item_sequence')
    sequence = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='canned_job_line_item_sequence_created', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='canned_job_line_item_sequence_updated', on_delete=models.DO_NOTHING, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'cannedjob_lineitem_sequence_new_03'
        ordering = ["-id",'sequence']
        indexes = [
            models.Index(fields=['canned_job', 'sequence', 'id'], name='canned_job_sequence_idx'),
        ]

    def __str__(self):
        return self.canned_job.canned_job_title