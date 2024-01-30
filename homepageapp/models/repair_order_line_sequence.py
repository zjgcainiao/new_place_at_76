from .base import models, InternalUser
from .repair_order import RepairOrdersNewSQL02Model
from .line_item import LineItemsNewSQL02Model




class RepairOrderLineItemSquencesNewSQL02Model(models.Model):
    ro_line_item_sequence_id = models.AutoField(primary_key=True)
    repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, models.CASCADE, blank=True, null=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, models.CASCADE, blank=True, null=True,related_name='lineitem_ro_line_item_sequence')
    sequence = models.IntegerField(null=True)

    ro_line_item_sequence_created_at = models.DateTimeField(auto_now_add=True)
    ro_line_item_sequence_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='ro_line_item_sequence_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='ro_line_item_sequence_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'repairorderlineitemsequences_new_03'
        ordering = ["-ro_line_item_sequence_id", 'repair_order', 'line_item']

