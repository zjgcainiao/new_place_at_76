from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model
from .labor_rate_description import LaborRateDescription


class LaborItemModel(models.Model):
    labor_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='lineitem_laboritem')
    labor_rate_description =  models.ForeignKey(LaborRateDescription, on_delete=models.SET_NULL, null=True, related_name='laboritem_laborratedescription')
    labor_item_is_user_entered_labor_rate = models.BooleanField(null=True) 
    labor_item_work_performed = models.TextField(blank=True, null=True)
    labor_item_hours_charged = models.DecimalField(
        max_digits=10, decimal_places=2)
    labor_item_symptom = models.CharField(
        max_length=4000, null=True, blank=True)
    labor_item_is_come_back_invoice = models.BooleanField(
        default=False, null=True)
    labor_item_parts_estimate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    labor_item_is_MPlg_item = models.IntegerField(default=False)
    labor_item_is_Changed_MPlg_item = models.BooleanField(default=False)

    labor_item_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='labor_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='labor_item_modified', on_delete=models.SET_NULL, null=True, blank=True)
    labor_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'laboritems_new_03'
        ordering = ["-labor_item_id"]
