from django.urls import reverse
from .base import models, InternalUser
from .line_item import LineItemsNewSQL02Model
from .repair_order_phase import RepairOrderPhasesNewSQL02Model
from .customer import CustomersNewSQL02Model
from .vehicle import VehiclesNewSQL02Model




class RepairOrdersNewSQL02Model(models.Model):
    # repair_order_new_uid_v01 = models.UUIDField(primary_key=True)  # models.UUIDField(primary_key=True)  # models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)
    repair_order_id = models.AutoField(primary_key=True)
    repair_order_phase = models.ForeignKey(
        RepairOrderPhasesNewSQL02Model, on_delete=models.SET_NULL, blank=True, null=True)
    # remove the `_id` from the field name. due to recent adding a foreign key.. by adding a foreign key field, Django will add '_id' for the field in the SQL data table.
    repair_order_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True)

    repair_order_vehicle = models.ForeignKey(
        VehiclesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True)

    repair_order_serviced_vehicle_location = models.CharField(
        max_length=36, null=True)
    repair_order_service_status = models.CharField(max_length=36, null=True)
    repair_order_scheduled_start_datetime = models.DateTimeField(null=True)
    # blank = False so this is a required field on form (pending testing)
    repair_order_billed_hours = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=False)
    repair_order_promise_datetime = models.DateTimeField(null=True)
    repair_order_is_printed = models.BooleanField(default=False)
    repair_order_invoice_is_printed = models.BooleanField(default=False)
    repair_order_serviced_vehicle_in_datetime = models.DateTimeField(
        null=True, blank=True)
    repair_order_serviced_vehicle_out_datetime = models.DateTimeField(
        null=True)
    repair_order_serviced_vehicle_hat = models.CharField(
        max_length=20, null=True)
    repair_order_posted_datetime = models.DateTimeField(null=True)
    repair_order_serviced_vehicle_odometer_in = models.BigIntegerField(
        null=True)
    repair_order_serviced_vehicle_odometer_out = models.BigIntegerField(
        null=True)
    repair_order_reference_number = models.CharField(
        max_length=30, null=True, blank=True)
    repair_order_receipt_printed_datetime = models.DateTimeField(null=True)
    repair_order_snapshot_is_tax_exempt = models.BooleanField(default=False)
    repair_order_aggr_notes = models.CharField(
        max_length=4000, null=True, blank=True)
    repair_order_observation_text_area = models.CharField(
        max_length=4000, null=True)
    repair_order_created_as_estimate = models.BooleanField(
        default=False)  # connecting to the estimates
    repair_order_snapshot_margin_pct = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_haz_waste_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_labor_sale_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_parts_sale_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_supply_from_shop_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_tax_haz_material_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_tax_supply_from_shop_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_total_tax_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_balance_due_adjusted = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_discounted_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_part_discounted_desc_id = models.IntegerField(
        null=True, blank=True)
    repair_order_snapshot_labor_discounted_desc_id = models.IntegerField(
        null=True, blank=True)
    repair_order_snapshot_order_total_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_calc_haz_waste_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_snapshot_calc_shop_supply_cost = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    repair_order_serviced_vehicle_engine_hours_in = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)
    repair_order_serviced_vehicle_engine_hours_out = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)
    repair_order_appointment_request_uid = models.CharField(
        max_length=50, null=True, blank=True)

    repair_order_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)
    repair_order_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='repair_order_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='repair_order_modified', on_delete=models.SET_NULL, null=True, blank=True)

    # added many-to-many relationship fields managers.
    lineitems = models.ManyToManyField(LineItemsNewSQL02Model, through='RepairOrderLineItemSquencesNewSQL02Model',
                                       related_name='lineitems')

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'repairorders_new_03'
        ordering = ["-repair_order_id"]
        verbose_name = 'repairorder'
        verbose_name_plural = 'repairorders'

    def get_absolute_url(self):
        return reverse('repair_order_detail', kwargs={'pk': self.pk})
