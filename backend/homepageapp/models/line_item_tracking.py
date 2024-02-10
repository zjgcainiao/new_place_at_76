from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model

LINE_ITEM_TYPE_CHOICES = (
    ('unassigned_type', 'Unassigned Line Item Type'),
    ('part', 'Part'),
    ('labor', 'Labor'),
)
# the intention is to have all line items with status_choice=completed
LINE_ITEM_STATUS_CHOICES = (
    ('not started', 'Not Started'),
    ('starting', 'Starting'),
    ('in_progress', 'In Progress'),
    ('initial_completion', 'Initial Completion'),
    ('repair_verifying', 'Repair Verifyng'),
    ('completed', 'Completed'),
)

# this model tracks the repair status of each line item.
class LineItemCompletionTracking(models.Model):

    id = models.BigAutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_completiontracking')

    line_item_assigned_technician = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True)
    line_item_technican_notes = models.TextField(null=True, blank=True)
    line_item_before_images = models.ImageField(
        upload_to='line_item_before_images/')
    line_item_after_images = models.ImageField(
        upload_to='line_item_after_images/')
    line_item_type = models.CharField(
        max_length=30, choices=LINE_ITEM_TYPE_CHOICES, default="unassigned_type")
    line_item_status = models.CharField(
        max_length=30, choices=LINE_ITEM_STATUS_CHOICES, default='not started')

    line_item_estimated_completion_at = models.DateTimeField(
        null=True, blank=True)

    # For tracking when this record was created.
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    udpated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'line_item_completion_tracking_new_03'
        ordering = ['-id', '-created_at']
