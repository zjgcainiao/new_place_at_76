from .base import models, InternalUser

from .account_class import AccountClassModel
from .category import CategoryModel

class PartsModel(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_description = models.CharField(max_length=500, null=True, blank=True)
    part_cost = models.DecimalField(max_digits=12, decimal_places=2)
    part_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_tax_exempt = models.BooleanField(default=False)
    part_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True)
    part_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='parts_accountclasses')
    part_comments = models.CharField(max_length=4000, null=True, blank=True)
    part_manufacturer_id = models.IntegerField(null=True)
    part_list_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_is_user_entered_price = models.DecimalField(
        max_digits=12, decimal_places=2)
    part_kit_id = models.IntegerField(null=True)
    part_is_MPLG_item = models.BooleanField(default=False)
    part_is_changed_MPLG_item = models.BooleanField(default=False)
    part_is_core = models.BooleanField(default=False)
    part_core_cost = models.DecimalField(max_digits=12, decimal_places=2)
    part_core_list_price = models.DecimalField(max_digits=12, decimal_places=2)
    part_fee_id = models.IntegerField(null=True)
    part_is_deleted = models.BooleanField(default=False)
    part_size = models.CharField(max_length=20, null=True, blank=True)
    part_is_tire = models.BooleanField(default=False)
    part_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='part_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='part_modified', on_delete=models.SET_NULL, null=True, blank=True)
    part_last_updated_at = models.DateTimeField(auto_now=True, null=True,)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'parts_new_03'
        ordering = ["-part_id"]

