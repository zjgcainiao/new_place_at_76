from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model

class LineItemAssignedTechnicanModel(models.Model):
    line_item_assigned_tech_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, models.CASCADE, blank=True, null=True)
    old_employee_id = models.IntegerField(null=True, blank=True)
    assigned_tech_hours_actual = models.DecimalField(
        max_digits=15, decimal_places=2)
    assigned_tech_hours_pay = models.DecimalField(
        max_digits=15, decimal_places=2)
    assigned_tech_comission = models.DecimalField(
        max_digits=15, decimal_places=2)

    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_assigned_tech_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_assigned_tech_modified', on_delete=models.SET_NULL, null=True, blank=True)
    line_item_assigned_tech_created_at = models.DateTimeField(
        auto_now_add=True)
    line_item_assigned_tech_last_change_date = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        # for naming you table
        db_table = "lineitemassignedtechnicans_new_03"
        ordering = ["-line_item"]
