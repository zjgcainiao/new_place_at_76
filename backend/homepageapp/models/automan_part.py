
from .base import models, InternalUser
from .account_class import AccountClassModel
from .category import CategoryModel
from decimal import Decimal


class AutomanPart(models.Model):
    id = models.AutoField(primary_key=True)
    is_tax_exempt = models.BooleanField(default=False)
    part_category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, related_name='automan_part_category')
    part_account_class = models.ForeignKey(
        AccountClassModel, on_delete=models.SET_NULL, null=True, related_name='automan_part_accountclasses')
    description = models.CharField(max_length=500, null=True, blank=True)
    is_tire = models.BooleanField(default=False)
    # new field to store tire info. is_tire can be integrated in the tire_info
    tire_info = models.JSONField(null=True, blank=True)
    comments = models.JSONField(null=True, blank=True)
    manufacturer_info = models.JSONField(null=True, blank=True)

    cost = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0.00))
    price = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0.00))
    list_price = models.DecimalField(max_digits=12, decimal_places=2)
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

    part_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='automan_part_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='automan_part_modified', on_delete=models.SET_NULL, null=True, blank=True)
    part_last_updated_at = models.DateTimeField(auto_now=True, null=True,)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'parts_new_03'
        ordering = ["-created_at"]
        verbose_name = 'Automan Part'
        verbose_name_plural = 'Automan Parts'
