from .base import models, InternalUser

from .account_class import AccountClassModel
from .canned_job import CannedJobsNewSQL02Model
from .category import CategoryModel
from decimal import Decimal

LINE_ITEM_TYPES = [
    ('part', 'Part Item'),
    ('labor', 'Labor Item'),
    ('note', 'Note Item'),
    ('unknown', 'unknown item type'),
]


class LineItemsNewSQL02Model(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    line_item_account_class = models.ForeignKey(
        AccountClassModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lineitem_accountclasses')
    line_item_category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lineitem_category')
    
    # 2023-10-01 newly added field
    line_item_type = models.CharField(
        max_length=10, choices=LINE_ITEM_TYPES, null=True)
    line_item_description = models.CharField(
        max_length=4000, null=True, blank=True)
    line_item_cost = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    line_item_sale = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    line_item_is_tax_exempt = models.BooleanField(default=False)
    line_item_has_no_commission = models.BooleanField(default=True)
    line_item_has_fixed_commission = models.BooleanField(default=False)
    line_item_order_revision_id = models.IntegerField(null=True, blank=True)
    # line_item_order_revision_id = models.ForeignKey(OrderRevisionNewSQL02Model, models.SET_NULL, blank=True, null=True)
    # any foreignKey field will add '_id' automatically when creating a sql data table. In the sql
    line_item_canned_job = models.ForeignKey(
        CannedJobsNewSQL02Model, models.SET_NULL, blank=True, null=True)
    line_item_labor_sale = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    line_item_part_sale = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    line_item_part_only_sale = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    line_item_labor_only_sale = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    line_item_sublet_sale = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    line_item_package_sale = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True)
    line_item_tire_fee = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=Decimal(0.00))
    line_item_parent_line_item = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    # added 2024-04-27
    assigned_to = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True,
        related_name='line_item_assigned_to',
        verbose_name='Assigned To')

    line_item_created_at = models.DateTimeField(auto_now_add=True)
    line_item_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='line_item_created',
        on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='line_item_modified',
        on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'lineitems_new_03'
        verbose_name = 'Line Item'
        verbose_name_plural = 'Line Items'
        ordering = ["-line_item_created_at"]
