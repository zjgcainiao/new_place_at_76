from .base import models, InternalUser
from .repair_order import RepairOrdersNewSQL02Model
from .vehicle import VehiclesNewSQL02Model

class OrderRevisionNewSQL02Model(models.Model):
    order_revision_id = models.AutoField(primary_key=True)
    order_revision_repair_order = models.ForeignKey(
        RepairOrdersNewSQL02Model, models.SET_NULL, blank=True, null=True, related_name='orderrevisions')
    order_revision_sub_estimate_number = models.IntegerField(
        blank=True, null=True)
    order_revision_date = models.DateTimeField(null=True)
    time_of_call = models.DateTimeField(null=True)
    order_revision_initiated_by = models.CharField(max_length=20, null=True)
    order_revision_by_service_writer_id = models.IntegerField(null=True)
    order_revision_authorizaton_by_name = models.CharField(
        max_length=50, null=True, blank=True)
    order_revision_number_called = models.CharField(max_length=50, null=True)
    order_revision_reason = models.CharField(max_length=200, null=True)
    order_revision_current_estimate = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_revision_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_vehicle_id = models.ForeignKey(
        VehiclesNewSQL02Model, models.SET_NULL, blank=True, null=True)
    order_revision_labor_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_parts_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_sublet_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_haz_waste_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_shop_supplies_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_amount_haz_mat = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_amount_shop_supplies = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_discounted_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tax_charged = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_tire_fee_amount = models.DecimalField(
        max_digits=15, decimal_places=2)
    order_revision_created_at = models.DateTimeField(auto_now_add=True)
    order_revision_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='order_revision_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='order_revision_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'orderrevisions_new_03'
        ordering = ["-order_revision_id"]