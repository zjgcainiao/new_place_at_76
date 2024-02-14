from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model
from .part import PartsModel


class PartItemModel(models.Model):
    part_item_id = models.AutoField(primary_key=True)
    line_item = models.ForeignKey(
        LineItemsNewSQL02Model, on_delete=models.CASCADE, related_name='lineitem_partitem')
    part_discount_description_id = models.IntegerField(null=True, blank=True)
    part_item_is_user_entered_unit_sale = models.BooleanField(default=False,
                                                              null=True, blank=True)
    part_item_is_user_entered_unit_cost = models.BooleanField(default=False,
                                                              null=True, blank=True)
    part_item_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_unit_list = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_unit_sale = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_unit_cost = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_part_no = models.CharField(max_length=100, 
                                         null=True, blank=True)
    part_item_part = models.ForeignKey(
        PartsModel, on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='part_partitem')
    part_item_is_confirmed = models.BooleanField(default=False,
                                                 null=True, blank=True)
    part_item_vendor_code = models.CharField(
        max_length=25,
        null=True, blank=True)
    part_item_vendor_id = models.IntegerField(null=True, blank=True)
    part_item_manufacture_id = models.IntegerField(null=True, blank=True)
    part_item_invoice_number = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_commission_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    part_item_is_committed = models.BooleanField(
        default=False,
        null=True, blank=True)
    part_item_is_quantity_confirmed = models.BooleanField(default=False,
                                                          null=True, blank=True)
    part_item_confirmed_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, 
        null=True, blank=True)
    part_item_is_part_ordered = models.BooleanField(default=False,
                                                    null=True, blank=True)
    part_item_is_core = models.BooleanField(default=False,null=True, blank=True)
    part_item_is_bundled_kit = models.BooleanField(default=False,
                                                   null=True, blank=True)
    part_item_is_MPlg_item = models.BooleanField(default=False,
                                                 null=True, blank=True)
    part_item_is_changed_MPlg_item = models.BooleanField(default=False,
                                                         null=True, blank=True)
    part_item_part_type = models.CharField(
        max_length=10, null=True, blank=True)
    part_item_size = models.CharField(max_length=20,
                                      null=True, blank=True)
    part_item_is_tire = models.BooleanField(default=False,
                                            null=True, blank=True)
    part_item_vendor_id = models.IntegerField(null=True, blank=True)
    part_item_meta = models.JSONField(null=True, blank=True)
    part_item_added_from_supplier = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_purchased_from_vendor = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_purchased_from_supplier = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_shipping_description = models.CharField(
        max_length=50, null=True, blank=True)
    part_item_shipping_cost = models.CharField(
        max_length=50, null=True, blank=True)

    part_item_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='part_item_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='part_item_modified', on_delete=models.SET_NULL, null=True, blank=True)
    part_item_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'partitems_new_03'
        ordering = ["-part_item_id"]
        verbose_name = 'partitem'
        verbose_name_plural = 'partitems'

