from .base import models, InternalUser


# ---- 2023-04-03 repairorderphase model is added ----
class RepairOrderPhasesNewSQL02Model(models.Model):
    repair_order_phase_id = models.AutoField(primary_key=True)
    repair_order_phase_description = models.CharField(max_length=50)
    repair_order_phase_created_at = models.DateTimeField(auto_now_add=True)
    repair_order_phase_last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='repair_order_phase_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='repair_order_phase_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.repair_order_phase_id}_{self.repair_order_phase_description}"
    class Meta:
        db_table = 'repairorderphases_new_03'
        ordering = ["repair_order_phase_id"]
        verbose_name = 'repairorderphase'
        verbose_name_plural = 'repairorderphases'